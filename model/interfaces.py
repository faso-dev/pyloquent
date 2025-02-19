from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Type, TypeVar, ClassVar, Generic

T = TypeVar('T', bound='ModelInterface')

class AttributeInterface(ABC):
    """Interface pour les attributs de modèle"""
    
    @abstractmethod
    def __get__(self, instance: Any, owner: Type) -> Any:
        pass
        
    @abstractmethod
    def __set__(self, instance: Any, value: Any) -> None:
        pass

class ModelInterface(ABC):
    """Interface pour les modèles"""
    
    _table_name: ClassVar[str]
    _connection: ClassVar[Any]
    _primary_key: ClassVar[str]
    
    @abstractmethod
    def __init__(self, **attributes: Dict[str, Any]) -> None:
        pass
        
    @abstractmethod
    def get_attribute(self, key: str) -> Any:
        pass
        
    @abstractmethod
    def set_attribute(self, key: str, value: Any) -> None:
        pass
        
    @classmethod
    @abstractmethod
    def find(cls: Type[T], id: Any) -> Optional[T]:
        pass 