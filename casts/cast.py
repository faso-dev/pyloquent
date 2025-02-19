from abc import ABC, abstractmethod
from typing import Any

class Cast(ABC):
    """
    Classe de base pour les casts d'attributs.
    
    Example:
        class JsonCast(Cast):
            def to_python(self, value):
                return json.loads(value) if value else {}
                
            def to_database(self, value):
                return json.dumps(value) if value else None
    """
    
    @abstractmethod
    def to_python(self, value: Any) -> Any:
        """
        Convertit la valeur de la base de données en type Python.
        
        Args:
            value: Valeur brute de la base de données
            
        Returns:
            Valeur convertie en type Python approprié
        """
        pass
        
    @abstractmethod
    def to_database(self, value: Any) -> Any:
        """
        Convertit la valeur Python en format base de données.
        
        Args:
            value: Valeur Python
            
        Returns:
            Valeur convertie pour stockage en base de données
        """
        pass 