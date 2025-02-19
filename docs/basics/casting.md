# Cast des Attributs

## Introduction

Le système de cast permet de transformer automatiquement les attributs lors de leur lecture/écriture dans la base de données.

## Casts Disponibles

```python
class User(Model):
    _casts = {
        'settings': 'json',        # Dict/JSON
        'is_active': 'bool',       # Booléen
        'score': 'float',          # Nombre flottant
        'created_at': 'datetime',  # DateTime
        'permissions': 'array'     # Liste
    }
```

## Création de Casts Personnalisés

```python
from pyloquent.casts import Cast
import json

class ArrayCast(Cast):
    def to_python(self, value):
        if value is None:
            return []
        if isinstance(value, list):
            return value
        try:
            return json.loads(value)
        except (TypeError, json.JSONDecodeError):
            return []
            
    def to_database(self, value):
        if value is None:
            return None
        return json.dumps(value)

# Enregistrement du cast
from pyloquent.casts import CastRegistry
CastRegistry.register('array', ArrayCast)
```

## Utilisation des Casts

```python
# Les casts sont automatiques
user = User(
    settings={'theme': 'dark'},  # Sera converti en JSON
    created_at='2023-01-01'     # Sera converti en datetime
)

# Lecture avec cast
print(user.settings['theme'])    # Accès direct au dict
print(user.created_at.year)      # Accès aux méthodes datetime

# Validation avec Pydantic
class UserSchema(BaseModel):
    settings: dict
    created_at: datetime
    
user_data = user.to_pydantic()  # Cast automatique pour Pydantic
``` 