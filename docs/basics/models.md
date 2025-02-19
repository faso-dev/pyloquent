# Modèles Pyloquent

## Introduction

Pyloquent fournit une implémentation élégante et intuitive de l'ORM SQLAlchemy. Chaque table de base de données a un "Modèle" correspondant qui est utilisé pour interagir avec cette table.

## Définition des modèles

```python
from pyloquent import Model
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

class User(Model):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Cast des attributs
    _casts = {
        'settings': 'json',
        'is_active': 'bool'
    }
    
    # Relations
    def posts(self):
        return self.has_many(Post, foreign_key='author_id')
```

## Conventions de nommage

Par défaut, Pyloquent utilisera le nom de la classe en minuscules et au pluriel comme nom de table. Vous pouvez personnaliser cela en définissant `__tablename__`.

## Timestamps

Par défaut, Pyloquent s'attend à ce que votre table ait les colonnes `created_at` et `updated_at`. Vous pouvez désactiver ce comportement :

```python
class User(Model):
    _timestamps = False
```

## Soft Deletes

Pour activer les soft deletes, ajoutez la colonne `deleted_at` et activez l'option :

```python
class User(Model):
    _soft_deletes = True
    deleted_at = Column(DateTime, nullable=True)
``` 