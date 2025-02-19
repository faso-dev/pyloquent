from typing import Any, List, Type, TypeVar
from .interfaces import MorphInterface
from ..types import ModelType

T = TypeVar('T', bound=ModelType)

class MorphMany(MorphInterface[T]):
    """
    Implémente une relation polymorphique one-to-many.
    
    Example:
        class Comment(Model):
            def commentable(self):
                return self.morph_to()
                
        class Post(Model):
            def comments(self):
                return self.morph_many(Comment, 'commentable')
                
        class Video(Model):
            def comments(self):
                return self.morph_many(Comment, 'commentable')
                
        # Utilisation
        post = Post.find(1)
        
        # Récupérer les commentaires
        comments = post.comments().with_('author').get()
        
        # Ajouter un commentaire
        post.comments().create({
            'body': 'Great post!',
            'author_id': user.id
        })
        
        # Requêtes avancées
        recent_comments = post.comments()\
            .where('is_approved', True)\
            .order_by('created_at', 'desc')\
            .take(5)\
            .get()
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
    
    def create_many(self, records: List[dict]) -> List[T]:
        """
        Crée plusieurs relations morphiques.
        
        Example:
            post.comments().create_many([
                {'body': 'First comment'},
                {'body': 'Second comment'}
            ])
        """
        return [self.create(attributes) for attributes in records]
    
    def delete_many(self, ids: List[Any] = None) -> int:
        """
        Supprime plusieurs relations morphiques.
        
        Example:
            # Supprime les commentaires spécifiés
            post.comments().delete_many([1, 2, 3])
            
            # Supprime tous les commentaires
            post.comments().delete_many()
        """
        query = self.add_constraints()
        
        if ids is not None:
            query.where_in('id', ids)
            
        return query.delete() 