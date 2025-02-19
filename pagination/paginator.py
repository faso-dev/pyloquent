from typing import List, TypeVar, Dict, Any, Optional
from math import ceil
from libs.pyloquent.exceptions import InvalidQueryException
from .interfaces import PaginatorInterface

T = TypeVar('T')

class Paginator(PaginatorInterface[T]):
    """
    Gère la pagination des résultats de requête.
    
    Example:
        # Pagination simple
        users = User.paginate(page=2, per_page=15)
        
        # Avec métadonnées
        result = users.to_dict()
        # {
        #     'data': [...],
        #     'meta': {
        #         'current_page': 2,
        #         'per_page': 15,
        #         'total': 45,
        #         'total_pages': 3,
        #         'has_more': True
        #     }
        # }
    """
    
    def __init__(
        self,
        items: List[T],
        total: int,
        page: int = 1,
        per_page: int = 15
    ) -> None:
        """
        Initialise un nouveau paginateur.
        
        Args:
            items: Éléments de la page courante
            total: Nombre total d'éléments
            page: Numéro de page courant
            per_page: Nombre d'éléments par page
        """
        self.items = items
        self.total = total
        self.per_page = per_page
        self.current_page = page
        self.last_page = ceil(total / per_page)
        
    @property
    def has_pages(self) -> bool:
        """Indique si la collection a plusieurs pages"""
        return self.last_page > 1
        
    @property
    def has_more_pages(self) -> bool:
        """Indique s'il y a des pages suivantes"""
        return self.current_page < self.last_page
        
    @property
    def previous_page(self) -> Optional[int]:
        """Retourne le numéro de la page précédente"""
        return self.current_page - 1 if self.current_page > 1 else None
        
    @property
    def next_page(self) -> Optional[int]:
        """Retourne le numéro de la page suivante"""
        return self.current_page + 1 if self.has_more_pages else None
    
    def url(self, page: int) -> str:
        """
        Génère l'URL pour une page donnée.
        
        Example:
            first_page_url = paginator.url(1)
            next_page_url = paginator.url(paginator.next_page)
        """
        if page < 1 or page > self.last_page:
            raise InvalidQueryException(f"Page {page} invalide")
            
        # À implémenter selon votre système de routing
        return f"?page={page}&per_page={self.per_page}"
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convertit le paginateur en dictionnaire.
        
        Returns:
            dict: {
                'data': List[T],
                'meta': {
                    'current_page': int,
                    'per_page': int,
                    'total': int,
                    'total_pages': int,
                    'has_more': bool,
                    'next_page': Optional[int],
                    'previous_page': Optional[int]
                }
            }
        """
        return {
            'data': self.items,
            'meta': {
                'current_page': self.current_page,
                'per_page': self.per_page,
                'total': self.total,
                'total_pages': self.last_page,
                'has_more': self.has_more_pages,
                'next_page': self.next_page,
                'previous_page': self.previous_page
            }
        } 