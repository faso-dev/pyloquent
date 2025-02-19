# Resources

## Introduction

Les Resources permettent de transformer vos modèles en structures JSON/dict avec un contrôle fin sur la sérialisation. Elles sont particulièrement utiles pour les APIs.

## Définition des Resources

```python
from pyloquent.resources import Resource
from pydantic import BaseModel
from datetime import datetime

class UserResource(Resource):
    """
    Transforme un User en JSON pour l'API.
    """
    
    # Schema Pydantic optionnel pour la validation
    class Schema(BaseModel):
        model_config = {'from_attributes': True}
        id: int
        name: str
        email: str
        posts_count: int | None
        
    def to_dict(self):
        return {
            'id': self.model.id,
            'name': self.model.name,
            'email': self.model.email,
            
            # Relations conditionnelles
            'posts': self.when_loaded('posts', 
                lambda posts: PostResource.collection(posts)
            ),
            
            # Champs calculés
            'posts_count': len(self.model.posts) if 'posts' in self.model.__dict__ else None,
            
            # Champs conditionnels
            'admin_data': self.when(
                self.model.is_admin,
                {
                    'permissions': self.model.permissions,
                    'last_login': self.model.last_login
                }
            )
        }
```

## Utilisation

```python
# Resource unique
user = User.find(1)
user_data = UserResource(user).to_dict()

# Collection de resources
users = User.query().with_('posts').get()
users_data = UserResource.collection(users).to_dict()

# Avec Pydantic
user_schema = UserResource(user).to_pydantic()
```

## Relations dans les Resources

```python
class PostResource(Resource):
    def to_dict(self):
        return {
            'id': self.model.id,
            'title': self.model.title,
            
            # Relation simple
            'author': self.when_loaded('author',
                lambda author: {
                    'id': author.id,
                    'name': author.name
                }
            ),
            
            # Relation avec resource
            'comments': self.when_loaded('comments',
                lambda comments: CommentResource.collection(comments)
            )
        }
``` 