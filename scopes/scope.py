from typing import Type, TypeVar, Any

from .interfaces import ScopeInterface, GlobalScopeInterface
from ..types import ModelType
from ..builder import QueryBuilder

T = TypeVar('T', bound=ModelType)

class Scope(ScopeInterface):
    """
    Classe de base pour définir des scopes de requête réutilisables.
    
    Example:
        class PublishedScope(Scope):
            def apply(self, builder, model):
                return builder.where('status', 'published')\
                            .where('published_at', '<=', datetime.now())
        
        class Post(Model):
            _global_scopes = [PublishedScope]
            
            @scope
            def popular(query):
                return query.where('views', '>', 1000)
            
        # Utilisation
        popular_posts = Post.popular().get()
    """
    
    def apply(self, query: QueryBuilder) -> QueryBuilder:
        """À surcharger dans les classes enfants"""
        return query

class GlobalScope(GlobalScopeInterface):
    """
    Un scope qui s'applique automatiquement à toutes les requêtes.
    
    Example:
        class SoftDeleteScope(GlobalScope):
            def apply(self, builder, model):
                return builder.where_null('deleted_at')
                
            def should_apply(self, model):
                return hasattr(model, '_soft_deletes')
    """
    
    def apply(self, query: QueryBuilder) -> QueryBuilder:
        """À surcharger dans les classes enfants"""
        return query
        
    def should_apply(self, model: Type[T]) -> bool:
        """Détermine si le scope doit être appliqué au modèle"""
        return True 