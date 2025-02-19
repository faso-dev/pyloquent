# Installation

## Configuration requise

- Python 3.8+
- SQLAlchemy 2.0+
- Pydantic 2.0+

## Installation via pip

```bash
pip install pyloquent
```

## Configuration de base

```python
from pyloquent import Model
from sqlalchemy import create_engine

# Configuration de la base de données
engine = create_engine('postgresql://user:pass@localhost/dbname')
Model.set_connection(engine)
```

## Configuration avec Alembic

```python
# alembic.ini
[alembic]
script_location = migrations
sqlalchemy.url = postgresql://user:pass@localhost/dbname

# migrations/env.py
from alembic import context
from pyloquent.model import Base

# Import vos modèles
from app.models import User, Post

target_metadata = Base.metadata
```
