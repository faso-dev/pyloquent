from typing import List, TypeVar, Dict, Any, Optional
from .interfaces import CursorPaginatorInterface

T = TypeVar('T')

class CursorPaginator(CursorPaginatorInterface[T]):
    """
    Pagination basée sur un curseur pour de meilleures performances.
    
    Example:
        # Première page
        posts = Post.order_by('id')\
            .cursor_paginate(limit=20)
            
        # Page suivante
        next_posts = Post.order_by('id')\
            .cursor_paginate(
                after=posts.next_cursor,
                limit=20
            )
    """
    
    def __init__(
        self,
        items: List[T],
        has_more: bool,
        cursor_field: str,
        limit: int,
        next_cursor: Optional[str] = None,
        previous_cursor: Optional[str] = None
    ) -> None:
        self.items = items
        self.has_more = has_more
        self.cursor_field = cursor_field
        self.limit = limit
        self.next_cursor = next_cursor
        self.previous_cursor = previous_cursor
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convertit le paginateur en dictionnaire.
        
        Returns:
            dict: {
                'data': List[T],
                'meta': {
                    'has_more': bool,
                    'next_cursor': Optional[str],
                    'previous_cursor': Optional[str]
                }
            }
        """
        return {
            'data': self.items,
            'meta': {
                'has_more': self.has_more,
                'next_cursor': self.next_cursor,
                'previous_cursor': self.previous_cursor
            }
        } 