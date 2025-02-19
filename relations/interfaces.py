from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, TypeVar, Generic, Type

from ..types import ModelType

T = TypeVar('T', bound=ModelType)

class RelationInterface(Generic[T], ABC):
    """Interface de base pour toutes les relations"""
    
    @abstractmethod
    def __init__(
        self,
        parent: Any,
        related: Type[T],
        foreign_key: str,
        local_key: str = 'id'
    ) -> None:
        pass
        
    @abstractmethod
    def get_results(self) -> List[T]:
        """Exécute la requête et retourne les résultats"""
        pass
        
    @abstractmethod
    def add_constraints(self) -> None:
        """Ajoute les contraintes spécifiques à la relation"""
        pass

class MorphInterface(RelationInterface[T], ABC):
    """Interface pour les relations polymorphiques"""
    
    @abstractmethod
    def __init__(
        self,
        parent: Any,
        related: Type[T],
        name: str,
        type_column: Optional[str] = None,
        id_column: Optional[str] = None
    ) -> None:
        pass 