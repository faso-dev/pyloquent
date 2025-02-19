from typing import List, TypeVar, Dict, Any, Optional
from math import ceil
from libs.pyloquent.pagination.paginator import Paginator
from libs.pyloquent.exceptions import InvalidQueryException

T = TypeVar('T')

class LengthAwarePaginator(Paginator[T]):
    """
    Paginateur avec connaissance du nombre total d'éléments.
    
    Cette classe étend le Paginator de base en ajoutant :
    - Nombre total d'éléments
    - Nombre total de pages
    - Liens de pagination
    - Métadonnées détaillées
    
    Example:
        # Création basique
        paginator = LengthAwarePaginator(
            items=users[0:15],
            total=total_users,
            page=1,
            per_page=15
        )
        
        # Avec métadonnées
        result = paginator.to_dict()
        # {
        #     'data': [...],
        #     'meta': {
        #         'current_page': 1,
        #         'per_page': 15,
        #         'total': 45,
        #         'total_pages': 3,
        #         'count': 15,
        #         'from': 1,
        #         'to': 15
        #     },
        #     'links': {
        #         'first': '?page=1',
        #         'last': '?page=3',
        #         'prev': null,
        #         'next': '?page=2'
        #     }
        # }
    """
    
    def __init__(
        self,
        items: List[T],
        total: int,
        page: int = 1,
        per_page: int = 15,
        path: Optional[str] = None,
        query_params: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Initialise le paginateur.
        
        Args:
            items: Éléments de la page courante
            total: Nombre total d'éléments
            page: Numéro de page courant
            per_page: Nombre d'éléments par page
            path: Chemin de base pour les liens
            query_params: Paramètres de requête additionnels
        """
        super().__init__(items, total, page, per_page)
        self.path = path
        self.query_params = query_params or {}
        
    @property
    def count(self) -> int:
        """Nombre d'éléments dans la page courante"""
        return len(self.items)
        
    @property
    def from_item(self) -> int:
        """Index du premier élément de la page"""
        if self.total == 0:
            return 0
        return (self.current_page - 1) * self.per_page + 1
        
    @property
    def to_item(self) -> int:
        """Index du dernier élément de la page"""
        if self.total == 0:
            return 0
        return min(self.from_item + self.count - 1, self.total)
    
    def get_url(self, page: int) -> Optional[str]:
        """
        Génère l'URL pour une page donnée.
        
        Args:
            page: Numéro de page
            
        Returns:
            str|None: URL de la page ou None si invalide
        """
        if page < 1 or page > self.last_page or not self.path:
            return None
            
        params = {**self.query_params, 'page': page, 'per_page': self.per_page}
        query = '&'.join(f"{k}={v}" for k, v in params.items())
        return f"{self.path}?{query}"
    
    def get_links(self) -> Dict[str, Optional[str]]:
        """
        Génère tous les liens de pagination.
        
        Returns:
            dict: {
                'first': str|None,
                'last': str|None,
                'prev': str|None,
                'next': str|None
            }
        """
        return {
            'first': self.get_url(1),
            'last': self.get_url(self.last_page),
            'prev': self.get_url(self.previous_page) if self.previous_page else None,
            'next': self.get_url(self.next_page) if self.next_page else None
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convertit le paginateur en dictionnaire.
        
        Returns:
            dict: {
                'data': List[T],
                'meta': dict,
                'links': dict  # Si path est défini
            }
        """
        result = {
            'data': self.items,
            'meta': {
                'current_page': self.current_page,
                'per_page': self.per_page,
                'total': self.total,
                'total_pages': self.last_page,
                'count': self.count,
                'from': self.from_item,
                'to': self.to_item,
                'has_more': self.has_more_pages
            }
        }
        
        if self.path:
            result['links'] = self.get_links()
            
        return result 