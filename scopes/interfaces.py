from abc import ABC, abstractmethod
from typing import Any, Type, TypeVar, Generic

from ..types import ModelType
from ..builder import QueryBuilder

T = TypeVar('T')

class ScopeInterface(Generic[T], ABC):
    """Interface pour les scopes"""
    
    @abstractmethod
    def apply(self, builder: QueryBuilder) -> QueryBuilder:
        """Applique le scope à la requête"""
        pass

class GlobalScopeInterface(ScopeInterface, ABC):
    """Interface pour les scopes globaux"""
    
    @abstractmethod
    def should_apply(self, model: Type[T]) -> bool:
        """Détermine si le scope doit être appliqué"""
        return True 