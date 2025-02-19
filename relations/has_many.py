from typing import Type, TypeVar, Any, List
from libs.pyloquent.relations.relation import Relation
from libs.pyloquent.builder import QueryBuilder

T = TypeVar('T')

class HasMany(Relation[T]):
    """
    Implémente une relation one-to-many.
    
    Example:
        class User(Model):
            def posts(self):
                return self.has_many(Post, 'user_id')
        
        # Utilisation
        user = User.find(1)
        
        # Récupérer tous les posts
        posts = user.posts().get()
        
        # Créer un nouveau post
        new_post = user.posts().create({
            'title': 'New Post',
            'content': 'Content...'
        })
        
        # Requêtes sur la relation
        recent_posts = user.posts()\
            .where('status', 'published')\
            .order_by('created_at', 'desc')\
            .take(5)\
            .get()
    """
    
    def __init__(
        self, 
        parent: Any, 
        related: Type[T], 
        foreign_key: str, 
        local_key: str = 'id'
    ):
        super().__init__(parent, related, foreign_key, local_key)
        
    def _add_constraints(self, query: QueryBuilder):
        """Ajoute les contraintes spécifiques HasMany"""
        query.where(self.foreign_key, '=', self.parent.get_attribute(self.local_key))
        
    def save(self, model: T):
        """Sauvegarde un modèle et l'associe à la relation"""
        self.fire_event('saving', model)
        model.setAttribute(self.foreign_key, self.parent.get_attribute(self.local_key))
        model.save()
        self.fire_event('saved', model)
        return model
        
    def create(self, attributes: dict) -> T:
        """
        Crée un nouveau modèle associé à cette relation.
        
        Args:
            attributes: Attributs du nouveau modèle
            
        Example:
            post = user.posts().create({
                'title': 'New Post',
                'content': 'Content...',
                'published': True
            })
        """
        self.fire_event('creating', attributes)
        model = self.related(**attributes)
        self.save(model)
        self.fire_event('created', model)
        return model
        
    def create_many(self, records: List[dict]) -> List[T]:
        """Crée plusieurs modèles associés"""
        return [self.create(record) for record in records]

    def get_results(self):
        """Obtient les résultats de la relation"""
        return self._get_base_query()\
            .where(self.foreign_key, '=', self.parent.get_key())\
            .get() 