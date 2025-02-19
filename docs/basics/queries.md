# Query Builder

## Introduction

Le Query Builder de Pyloquent fournit une interface fluide pour construire des requêtes SQL. Il peut être utilisé pour effectuer la plupart des opérations de base de données.

## Récupération de résultats

```python
# Tous les enregistrements
users = User.query().get()

# Filtrage simple
active_users = User.query()\
    .where('is_active', True)\
    .get()

# Filtres multiples
users = User.query()\
    .where('age', '>=', 18)\
    .where('status', 'active')\
    .order_by('created_at', 'desc')\
    .get()

# Premier résultat
user = User.query()\
    .where('email', 'john@example.com')\
    .first()

# Pagination
users = User.query()\
    .paginate(page=1, per_page=15)
```

## Clauses Where

```python
# Opérateurs de comparaison
User.query()\
    .where('age', '>', 18)\
    .where('status', '!=', 'banned')\
    .get()

# Where In
User.query()\
    .where_in('id', [1, 2, 3])\
    .get()

# Where Between
User.query()\
    .where_between('created_at', ['2023-01-01', '2023-12-31'])\
    .get()

# Where Null
User.query()\
    .where_null('deleted_at')\
    .get()

# Conditions OR
User.query()\
    .where('status', 'active')\
    .or_where('role', 'admin')\
    .get()
```

## Agrégations

```python
# Comptage
count = User.query().count()

# Autres agrégations
avg_age = User.query().avg('age')
total = Order.query().sum('amount')
oldest = User.query().max('created_at')

# Groupement
stats = Order.query()\
    .select('status')\
    .select_raw('COUNT(*) as count')\
    .group_by('status')\
    .having('count', '>', 100)\
    .get()
```

## Scopes

```python
class User(Model):
    @classmethod
    def active(cls, query):
        return query.where('is_active', True)
    
    @classmethod
    def popular(cls, query):
        return query.where_has('posts', lambda q:
            q.where('views', '>', 1000)
        )

# Utilisation
popular_users = User.query()\
    .active()\
    .popular()\
    .get()
``` 