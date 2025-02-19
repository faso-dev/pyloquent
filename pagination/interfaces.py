from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, TypeVar, Generic

T = TypeVar('T')

class PaginatorInterface(Generic[T], ABC):
    """Interface de base pour les paginateurs"""
    
    @abstractmethod
    def __init__(
        self,
        items: List[T],
        total: int,
        page: int = 1,
        per_page: int = 15
    ) -> None:
        pass
        
    @property
    @abstractmethod
    def has_more_pages(self) -> bool:
        """Indique s'il y a des pages suivantes"""
        pass
        
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convertit le paginateur en dictionnaire"""
        pass

class CursorPaginatorInterface(Generic[T], ABC):
    """Interface pour la pagination par curseur"""
    
    @abstractmethod
    def __init__(
        self,
        items: List[T],
        has_more: bool,
        cursor_field: str,
        limit: int,
        next_cursor: Optional[str] = None,
        previous_cursor: Optional[str] = None
    ) -> None:
        pass 