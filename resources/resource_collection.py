from typing import List, Dict, Any, TypeVar, Optional

from .interfaces import ResourceCollectionInterface, ResourceInterface
from ..pagination import Paginator
from ..types import ModelType

T = TypeVar('T', bound=ModelType)

class ResourceCollection(ResourceCollectionInterface[T]):
    """
    Collection de resources avec fonctionnalités supplémentaires.
    
    Example:
        resources = UserResource.collection(users)
        
        # Conversion en dictionnaire
        data = resources.to_dict()
        
        # Avec pagination
        result = resources.paginate(
            page=1,
            per_page=15,
            path='/api/users'
        )
        
        # Avec métadonnées
        result = resources.additional({
            'total_admins': resources.filter(lambda r: r.model.is_admin).count()
        }).to_dict()
    """
    
    def __init__(self, items: List[ResourceInterface[T]]) -> None:
        self.items = items
        self._additional: Dict[str, Any] = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convertit la collection en dictionnaire.
        
        Returns:
            dict: {
                'data': List[dict],
                'meta': dict  # Si des métadonnées sont présentes
            }
        """
        result = {
            'data': [resource.to_dict() for resource in self.items]
        }
        
        if self._additional:
            result['meta'] = self._additional
            
        return result
    
    def additional(self, data: Dict[str, Any]) -> 'ResourceCollection':
        """
        Ajoute des métadonnées à la collection.
        
        Example:
            resources.additional({
                'total': resources.count(),
                'filtered': len(resources.filter(predicate))
            })
        """
        self._additional.update(data)
        return self
    
    def paginate(
        self,
        page: int = 1,
        per_page: int = 15,
        path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Pagine la collection.
        
        Returns:
            dict: {
                'data': List[dict],
                'meta': {
                    'current_page': int,
                    'per_page': int,
                    'total': int,
                    'total_pages': int,
                    'has_more': bool
                },
                'links': {  # Si path fourni
                    'first': str,
                    'last': str,
                    'prev': Optional[str],
                    'next': Optional[str]
                }
            }
        """
        paginator = Paginator(self.items, len(self.items), page, per_page)
        
        result = {
            'data': [resource.to_dict() for resource in paginator.items],
            'meta': {
                'current_page': paginator.current_page,
                'per_page': paginator.per_page,
                'total': paginator.total,
                'total_pages': paginator.last_page,
                'has_more': paginator.has_more_pages
            }
        }
        
        if path:
            result['links'] = self._get_pagination_links(paginator, path)
            
        return result
    
    def _get_pagination_links(self, paginator: Paginator, path: str) -> Dict[str, str]:
        """Génère les liens de pagination."""
        return {
            'first': f"{path}?page=1&per_page={paginator.per_page}",
            'last': f"{path}?page={paginator.last_page}&per_page={paginator.per_page}",
            'prev': f"{path}?page={paginator.previous_page}&per_page={paginator.per_page}" 
                   if paginator.previous_page else None,
            'next': f"{path}?page={paginator.next_page}&per_page={paginator.per_page}"
                   if paginator.next_page else None
        } 