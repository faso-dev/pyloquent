from abc import ABC, abstractmethod
from typing import Any, List, Dict, Optional, Type

from ..types import ModelType

class BuilderInterface(ABC):
    """Interface de base pour tous les builders"""
    
    @abstractmethod
    def __init__(self, model: Type[ModelType]):
        self.model = model
        
    @abstractmethod
    def get(self) -> List[ModelType]:
        """Exécute la requête et retourne les résultats"""
        pass
        
    @abstractmethod
    def first(self) -> Optional[ModelType]:
        """Retourne le premier résultat"""
        pass 