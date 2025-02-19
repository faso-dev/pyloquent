from typing import Dict, Type, Any
from .interfaces import CastInterface

class CastRegistry:
    """
    Registre global des casts disponibles.
    
    Example:
        # Ajouter un cast personnalisé
        CastRegistry.register('array', ArrayCast)
        
        # Utiliser dans un modèle
        class User(Model):
            _casts = {
                'permissions': 'array'
            }
    """
    
    _casts: Dict[str, Type[CastInterface]] = {}
    
    @classmethod
    def register(cls, name: str, cast: Type[CastInterface]):
        """Enregistre un nouveau type de cast."""
        cls._casts[name] = cast
        
    @classmethod
    def get(cls, name: str) -> Type[CastInterface]:
        """Récupère une classe de cast par son nom."""
        if name not in cls._casts:
            raise ValueError(f"Cast non trouvé: {name}")
        return cls._casts[name]
        
    @classmethod
    def cast(cls, value: Any, cast_type: str) -> Any:
        """
        Applique un cast à une valeur.
        
        Example:
            value = CastRegistry.cast('{"key": "value"}', 'json')
            # Retourne {'key': 'value'}
        """
        cast_class = cls.get(cast_type)
        return cast_class().to_python(value)

# Enregistrement des casts par défaut
from .json_cast import JsonCast
from .datetime_cast import DateTimeCast

CastRegistry._casts.update({
    'json': JsonCast,
    'datetime': DateTimeCast,
    'bool': lambda x: bool(x),
    'int': lambda x: int(x) if x is not None else None,
    'float': lambda x: float(x) if x is not None else None,
    'str': lambda x: str(x) if x is not None else None,
}) 