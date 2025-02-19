from typing import Dict, Type, TypeVar, List, Optional
from .interfaces import ModelInterface
from ..exceptions import PyloquentException

T = TypeVar('T')

class ModelRegistry:
    """Registre global des modèles"""
    
    _models: Dict[str, Type[T]] = {}
    _aliases: Dict[str, str] = {}
    
    @classmethod
    def add(
        cls,
        name: str,
        model: Type[T],
        aliases: Optional[List[str]] = None
    ) -> None:
        """Enregistre un modèle dans le registre"""
        cls._models[name.lower()] = model
        
        if aliases:
            for alias in aliases:
                cls._aliases[alias.lower()] = name.lower()
                
    @classmethod
    def resolve(cls, name: str) -> Type[T]:
        """Résout un nom de modèle en classe"""
        name = name.lower()
        if name in cls._aliases:
            name = cls._aliases[name]
            
        if name not in cls._models:
            raise PyloquentException(f"Model not found: {name}")
            
        return cls._models[name]
    
    @classmethod
    def register(cls, model: Type[T]) -> Type[T]:
        """Décorateur pour enregistrer un modèle"""
        name = model.__name__.lower()
        cls.add(name, model)
        return model 