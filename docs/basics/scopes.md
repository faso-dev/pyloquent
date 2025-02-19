# Scopes

## Introduction

Les scopes permettent d'encapsuler des contraintes de requête communes pour les réutiliser facilement dans votre application.

## Définition des Scopes

```python
from pyloquent.scopes import Scope, GlobalScope

# Scope local
class User(Model):
    @classmethod
    def active(cls, query):
        return query.where('is_active', True)
        
    @classmethod
    def popular(cls, query):
        return query.where_has('posts', lambda q:
            q.where('views', '>', 1000)
        )

# Scope global
class PublishedScope(GlobalScope):
    def apply(self, builder, model):
        return builder.where('status', 'published')\
                     .where('published_at', '<=', datetime.now())

class Post(Model):
    _global_scopes = [PublishedScope]
```

## Utilisation des Scopes

```python
# Scope local
active_users = User.query()\
    .active()\
    .get()

# Combinaison de scopes
popular_active_users = User.query()\
    .active()\
    .popular()\
    .get()

# Désactiver un scope global
all_posts = Post.query()\
    .without_global_scope(PublishedScope)\
    .get()

# Scope dynamique
def by_type(query, type):
    return query.where('type', type)

users = User.query()\
    .scope(by_type, 'admin')\
    .get()
```

## Scopes avec Paramètres

```python
class User(Model):
    @classmethod
    def of_type(cls, query, type):
        return query.where('type', type)
        
    @classmethod
    def created_between(cls, query, start, end):
        return query.where_between('created_at', [start, end])

# Utilisation
users = User.query()\
    .of_type('admin')\
    .created_between('2023-01-01', '2023-12-31')\
    .get()
``` 