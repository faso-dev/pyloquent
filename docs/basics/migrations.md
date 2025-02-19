# Migrations

## Introduction

Les migrations permettent de versionner votre schéma de base de données. Pyloquent s'intègre avec Alembic pour fournir une API simple et expressive.

## Création de Migrations

```bash
# Créer une nouvelle migration
alembic revision -m "create_users_table"
```

## Structure des Migrations

```python
from alembic import op
import sqlalchemy as sa
from pyloquent.migrations import Migration

def upgrade():
    Migration.create_table(
        'users',
        id=sa.Integer().primary_key(),
        name=sa.String(100).nullable(False),
        email=sa.String(255).unique(),
        password=sa.String(255),
        is_active=sa.Boolean().default(True),
        timestamps=True  # Ajoute created_at et updated_at
    )
    
    # Ajouter un index
    op.create_index('idx_users_email', 'users', ['email'])

def downgrade():
    op.drop_table('users')
```

## Relations dans les Migrations

```python
def upgrade():
    # Table principale
    Migration.create_table(
        'posts',
        id=sa.Integer().primary_key(),
        title=sa.String(200),
        content=sa.Text(),
        author_id=sa.Integer().foreign_key('users.id'),
        timestamps=True
    )
    
    # Table pivot pour many-to-many
    Migration.create_table(
        'post_tags',
        id=sa.Integer().primary_key(),
        post_id=sa.Integer().foreign_key('posts.id'),
        tag_id=sa.Integer().foreign_key('tags.id'),
        timestamps=True
    )
    
    # Index unique
    op.create_unique_constraint(
        'uq_post_tags',
        'post_tags',
        ['post_id', 'tag_id']
    )
```

## Opérations Courantes

```python
def upgrade():
    # Ajouter une colonne
    Migration.add_column('users', 'phone', sa.String(20))
    
    # Renommer une colonne
    Migration.rename_column('users', 'email', 'email_address')
    
    # Modifier une colonne
    with op.batch_alter_table('users') as batch_op:
        batch_op.alter_column('name',
            existing_type=sa.String(50),
            type_=sa.String(100)
        )
    
    # Supprimer une colonne
    Migration.drop_column('users', 'old_field')
```

## Exécution des Migrations

```bash
# Appliquer toutes les migrations
alembic upgrade head

# Revenir en arrière d'une migration
alembic downgrade -1

# Revenir à une révision spécifique
alembic downgrade <revision>

# Voir le statut des migrations
alembic current
``` 