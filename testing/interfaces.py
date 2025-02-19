from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Type, TypeVar, Generic

from ..types import ModelType

T = TypeVar('T', bound=ModelType)

class FactoryInterface(Generic[T], ABC):
    """Interface pour les factories de modèles"""
    
    @abstractmethod
    def definition(self) -> Dict[str, Any]:
        """Définit les attributs par défaut"""
        pass
        
    @abstractmethod
    def make(self, **attributes) -> T:
        """Crée une instance sans sauvegarder"""
        pass
        
    @abstractmethod
    def create(self, **attributes) -> T:
        """Crée et sauvegarde une instance"""
        pass
        
    @abstractmethod
    def make_many(self, count: int, **attributes) -> List[T]:
        """Crée plusieurs instances sans sauvegarder"""
        pass
        
    @abstractmethod
    def create_many(self, count: int, **attributes) -> List[T]:
        """Crée et sauvegarde plusieurs instances"""
        pass

class SeederInterface(ABC):
    """Interface pour les seeders"""
    
    @abstractmethod
    def run(self) -> None:
        """Exécute le seeder"""
        pass 