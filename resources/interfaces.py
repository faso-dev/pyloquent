from abc import ABC, abstractmethod
from typing import Any, Dict, List, TypeVar, Generic, Optional, Type

from ..types import ModelType

T = TypeVar('T', bound=ModelType)

class ResourceInterface(Generic[T], ABC):
    """Base interface for resources"""
    
    @abstractmethod
    def __init__(self, model: T) -> None:
        pass
        
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convert to a dictionary"""
        pass
        
    @classmethod
    @abstractmethod
    def collection(cls, models: List[T]) -> 'ResourceCollectionInterface':
        """Create a collection of resources"""
        pass

class ResourceCollectionInterface(Generic[T], ABC):
    """Interface for resource collections"""
    
    @abstractmethod
    def __init__(self, items: List[ResourceInterface[T]]) -> None:
        pass
        
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convert the collection to a dictionary"""
        pass
        
    @abstractmethod
    def paginate(
        self,
        page: int = 1,
        per_page: int = 15,
        path: Optional[str] = None
    ) -> Dict[str, Any]:
        """Paginate the collection"""
        pass 