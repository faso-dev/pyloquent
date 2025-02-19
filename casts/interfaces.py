from abc import ABC, abstractmethod
from typing import Any, TypeVar, Generic

CastValueType = TypeVar('CastValueType')

class CastInterface(Generic[CastValueType], ABC):
    """Interface de base pour tous les casts"""
    
    @abstractmethod
    def to_python(self, value: Any) -> CastValueType:
        """Convertit une valeur de la base de données en type Python"""
        pass
        
    @abstractmethod
    def to_database(self, value: CastValueType) -> Any:
        """Convertit une valeur Python en format base de données"""
        pass 