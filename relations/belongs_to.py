from typing import Type, TypeVar, Any, Optional
from .relation import Relation
from ..types import ModelType
from ..builder import QueryBuilder

T = TypeVar('T', bound=ModelType)

class BelongsTo(Relation[T]):
    """
    Implémente une relation inverse one-to-many ou one-to-one.
    
    Example:
        class Post(Model):
            def author(self):
                return self.belongs_to(User, 'author_id')
                
        # Utilisation basique
        post = Post.find(1)
        author = post.author().first()
        
        # Avec chargement eager
        posts = Post.with_('author').get()
        
        # Requêtes sur la relation
        posts = Post.query()\
            .where_has('author', lambda q: 
                q.where('is_verified', True)
            )\
            .get()
            
        # Association
        post.author().associate(user)
        post.author().dissociate()
    """
    
    def __init__(
        self,
        parent: Any,
        related: Type[T],
        foreign_key: str,
        owner_key: str = 'id'
    ):
        super().__init__(parent, related, foreign_key, owner_key)
        
    def add_constraints(self, query: QueryBuilder) -> QueryBuilder:
        """Ajoute les contraintes spécifiques BelongsTo"""
        try:
            foreign_key_value = getattr(self.parent, self.foreign_key)
            if foreign_key_value is None:
                raise RuntimeError(
                    f"Foreign key '{self.foreign_key}' is None on {self.parent.__class__.__name__}. "
                    "Make sure the foreign key has a value."
                )
            return query.where(self.local_key, '=', foreign_key_value)
        except AttributeError:
            raise RuntimeError(
                f"Foreign key '{self.foreign_key}' not found on {self.parent.__class__.__name__}. "
                "Make sure the column is properly defined."
            )
        
    def associate(self, model: T) -> bool:
        """Associe un modèle à cette relation"""
        self.fire_event('associating', model)
        self.parent.set_attribute(self.foreign_key, model.get_attribute(self.local_key))
        result = self.parent.save()
        self.fire_event('associated', model)
        return result
        
    def dissociate(self) -> bool:
        """Supprime l'association"""
        self.fire_event('dissociating')
        self.parent.set_attribute(self.foreign_key, None)
        result = self.parent.save()
        self.fire_event('dissociated')
        return result
        
    def get_results(self) -> Optional[T]:
        """Obtient le résultat de la relation"""
        return self.first() 