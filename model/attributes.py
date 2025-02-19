from datetime import datetime
from typing import Any, Dict, Type, Optional, Generic, TypeVar
from uuid import UUID
from .interfaces import AttributeInterface

T = TypeVar('T')

class Attribute(AttributeInterface, Generic[T]):
    """
    Descripteur pour les attributs de modèle avec cast automatique.
    
    Example:
        class User(Model):
            id = Attribute[int]('id')
            name = Attribute[str]('name')
            is_active = Attribute[bool]('is_active', default=True)
    """
    
    def __init__(
        self,
        name: str,
        type_: Type[T] = Any,
        nullable: bool = True,
        default: Optional[T] = None
    ):
        self.name = name
        self.type = type_
        self.nullable = nullable
        self.default = default
        
    def __get__(self, instance: Any, owner: Type) -> T:
        if instance is None:
            return self
            
        value = instance.get_attribute(self.name)
        if value is None:
            return self.default
            
        return self._cast_value(value)
        
    def __set__(self, instance: Any, value: Any) -> None:
        if not self.nullable and value is None:
            raise ValueError(f"{self.name} cannot be null")
            
        instance.set_attribute(self.name, value)
        
    def _cast_value(self, value: Any) -> T:
        if value is None:
            return None
            
        if isinstance(value, self.type):
            return value
            
        try:
            return self.type(value)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot cast {value} to {self.type.__name__}") from e

class AttributeCaster:
    """Gestionnaire de cast d'attributs"""
    
    _casts: Dict[str, Type] = {
        'int': int,
        'float': float,
        'str': str,
        'bool': bool,
        'datetime': datetime,
        'uuid': UUID,
    }
    
    @classmethod
    def register(cls, name: str, cast_type: Type) -> None:
        """Enregistre un nouveau type de cast"""
        cls._casts[name] = cast_type
        
    @classmethod
    def cast(cls, value: Any, cast_type: str) -> Any:
        """Cast une valeur vers un type spécifique"""
        if cast_type not in cls._casts:
            raise ValueError(f"Unsupported cast type: {cast_type}")
            
        caster = cls._casts[cast_type]
        return caster(value) if value is not None else None 