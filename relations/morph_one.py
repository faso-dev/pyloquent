from typing import Any, Type, TypeVar
from libs.pyloquent.relations.relation import Relation
from ..types import ModelType

T = TypeVar('T', bound=ModelType)

class MorphOne(Relation[T]):
    """
    Implémente une relation polymorphique one-to-one.
    
    Example:
        class Image(Model):
            def imageable(self):
                return self.morph_to()  # Relation polymorphique inverse
                
        class User(Model):
            def avatar(self):
                return self.morph_one(Image, 'imageable')
                
        class Post(Model):
            def thumbnail(self):
                return self.morph_one(Image, 'imageable')
                
        # Utilisation
        user = User.find(1)
        avatar = user.avatar().first()
        
        # Création
        user.avatar().create({
            'path': '/images/avatar.jpg',
            'size': 1024
        })
    """
    
    def __init__(
        self,
        parent: Any,
        related: Type[T],
        name: str,
        type_column: str = None,
        id_column: str = None
    ):
        super().__init__(parent, related)
        self.morph_type = name
        self.type_column = type_column or f"{name}_type"
        self.id_column = id_column or f"{name}_id"
        
    def add_constraints(self):
        """Ajoute les contraintes morphiques"""
        parent_type = self.parent.__class__.__name__
        
        return self.where(self.type_column, parent_type)\
                   .where(self.id_column, self.parent.get_key())
                   
    def create(self, attributes: dict) -> T:
        """
        Crée une nouvelle relation morphique.
        
        Example:
            post.thumbnail().create({
                'path': '/images/post.jpg',
                'alt': 'Post thumbnail'
            })
        """
        self.fire_event('creating', attributes)
        
        attributes[self.type_column] = self.parent.__class__.__name__
        attributes[self.id_column] = self.parent.get_key()
        
        instance = self.related.create(attributes)
        
        self.fire_event('created', instance)
        return instance 