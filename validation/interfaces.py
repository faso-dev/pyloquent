from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union, TypeVar, Generic

T = TypeVar('T')

class RuleInterface(ABC):
    """Interface pour les règles de validation"""
    
    @abstractmethod
    def validate(self, attribute: str, value: Any) -> Union[bool, str]:
        """Valide une valeur"""
        pass
        
    @abstractmethod
    def message(self, attribute: str, value: Any) -> str:
        """Message d'erreur personnalisé"""
        pass

class ValidatorInterface(ABC):
    """Interface pour les validateurs"""
    
    @abstractmethod
    def validate(self) -> bool:
        """Exécute la validation"""
        pass
        
    @abstractmethod
    def fails(self) -> bool:
        """Vérifie si la validation a échoué"""
        pass
        
    @abstractmethod
    def errors(self) -> Dict[str, List[str]]:
        """Retourne les erreurs de validation"""
        pass 