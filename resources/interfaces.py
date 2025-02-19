from abc import ABC, abstractmethod
from typing import Any, Dict, List, TypeVar, Generic, Optional, Type
from pydantic import BaseModel

from ..types import ModelType

T = TypeVar('T', bound=ModelType)

class ResourceInterface(Generic[T], ABC):
    """Interface de base pour les resources"""
    
    @abstractmethod
    def __init__(self, model: T) -> None:
        pass
        
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convertit en dictionnaire"""
        pass
        
    @classmethod
    @abstractmethod
    def collection(cls, models: List[T]) -> 'ResourceCollectionInterface':
        """Crée une collection de resources"""
        pass

class ResourceCollectionInterface(Generic[T], ABC):
    """Interface pour les collections de resources"""
    
    @abstractmethod
    def __init__(self, items: List[ResourceInterface[T]]) -> None:
        pass
        
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convertit la collection en dictionnaire"""
        pass
        
    @abstractmethod
    def paginate(
        self,
        page: int = 1,
        per_page: int = 15,
        path: Optional[str] = None
    ) -> Dict[str, Any]:
        """Pagine la collection"""
        pass 