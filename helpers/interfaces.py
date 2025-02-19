from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional, TypeVar, Generic, Union

T = TypeVar('T')

class CollectionInterface(Generic[T], ABC):
    """Interface pour les collections"""
    
    @abstractmethod
    def all(self) -> List[T]:
        """Retourne tous les éléments"""
        pass
        
    @abstractmethod
    def avg(self, key: Optional[str] = None) -> float:
        """Calcule la moyenne"""
        pass
        
    @abstractmethod
    def contains(self, key: Union[str, Callable[[T], bool]], value: Any = None) -> bool:
        """Vérifie si un élément existe"""
        pass
        
    @abstractmethod
    def count(self) -> int:
        """Compte les éléments"""
        pass
        
    @abstractmethod
    def first(self, callback: Optional[Callable[[T], bool]] = None) -> Optional[T]:
        """Retourne le premier élément"""
        pass
        
    @abstractmethod
    def last(self, callback: Optional[Callable[[T], bool]] = None) -> Optional[T]:
        """Retourne le dernier élément"""
        pass 