# Relations

## Introduction

Pyloquent fournit une gestion puissante des relations entre vos modèles. Les relations sont définies comme des méthodes dans vos modèles.

## Définition des relations

### One To One

```python
class User(Model):
    def profile(self):
        return self.has_one(Profile, foreign_key='user_id')

class Profile(Model):
    def user(self):
        return self.belongs_to(User, foreign_key='user_id')
```

### One To Many

```python
class User(Model):
    def posts(self):
        return self.has_many(Post, foreign_key='author_id')

class Post(Model):
    def author(self):
        return self.belongs_to(User, foreign_key='author_id')
```

### Many To Many

```python
class User(Model):
    def roles(self):
        return self.belongs_to_many(
            Role,
            table='user_roles',
            foreign_pivot_key='role_id',
            related_pivot_key='user_id'
        )

# Utilisation
user.roles().attach(role_id)
user.roles().detach(role_id)
user.roles().sync([1, 2, 3])
```

## Eager Loading

Pour éviter le problème N+1, utilisez le chargement eager :

```python
# Chargement simple
users = User.with_('posts', 'profile').get()

# Chargement avec contraintes
users = User.with_('posts', lambda q: 
    q.where('is_published', True)
     .order_by('created_at', 'desc')
).get()

# Chargement imbriqué
users = User.with_({
    'posts': {
        'where': [['is_published', True]],
        'with': ['comments']
    }
}).get()
``` 