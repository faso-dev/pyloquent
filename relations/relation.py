from typing import Any, Type, TypeVar, List, Dict, Optional, TYPE_CHECKING
from abc import abstractmethod

if TYPE_CHECKING:
    from ..builder import QueryBuilder

from .interfaces import RelationInterface
from ..types import ModelType
from ..builder import QueryBuilder

T = TypeVar('T', bound=ModelType)

class Relation(RelationInterface[T]):
    """Classe de base pour toutes les relations"""
    
    def __init__(
        self,
        parent: Any,
        related: Type[T],
        foreign_key: str,
        local_key: str = 'id'
    ) -> None:
        self.parent = parent
        self.related = related
        self.foreign_key = foreign_key
        self.local_key = local_key
        self._query: Optional[QueryBuilder] = None
        self._constraints: List[callable] = []
        self._with_global_scopes: bool = True
        self._with_trashed: bool = False
        
    @abstractmethod
    def add_constraints(self, query: QueryBuilder) -> QueryBuilder:
        """Ajoute les contraintes spécifiques à la relation"""
        pass
        
    def get_query(self) -> QueryBuilder:
        """Obtient la requête de base pour la relation"""
        query = self.related.query()
        
        if not self._with_global_scopes:
            query.without_global_scopes()
            
        if self._with_trashed:
            query.with_trashed()
            
        return self.add_constraints(query)
        
    def get(self) -> List[T]:
        """Exécute la requête et retourne les résultats"""
        return self.get_query().get()
        
    def first(self) -> Optional[T]:
        """Retourne le premier résultat"""
        return self.get_query().first()
        
    def get_results(self) -> Any:
        """Obtient les résultats de la relation"""
        return self.get()
        
    def add_constraint(self, callback: callable) -> None:
        """
        Ajoute une contrainte à la relation.
        
        Args:
            callback: Fonction qui reçoit le QueryBuilder
            
        Example:
            posts.add_constraint(lambda q: 
                q.where('status', 'published')
                 .where('views', '>', 100)
            )
        """
        self._constraints.append(callback)
        
    def find(self, id: Any) -> Optional[T]:
        """
        Trouve un modèle par son ID dans la relation.
        
        Example:
            post = user.posts().find(5)
        """
        return self.where('id', id).first()
        
    def exists(self) -> bool:
        """
        Vérifie si la relation a des résultats.
        
        Example:
            if user.posts().exists():
                print("L'utilisateur a des posts")
        """
        return self.count() > 0
        
    def count(self) -> int:
        """
        Compte le nombre de résultats.
        
        Example:
            posts_count = user.posts().count()
        """
        return self.query.count()
        
    def update(self, attributes: Dict[str, Any]) -> int:
        """
        Met à jour tous les modèles de la relation.
        
        Example:
            # Marque tous les posts comme publiés
            user.posts().update({
                'is_published': True,
                'published_at': datetime.now()
            })
        """
        return self.query.update(attributes)
        
    def delete(self) -> int:
        """
        Supprime tous les modèles de la relation.
        
        Example:
            # Supprime tous les posts de l'utilisateur
            user.posts().delete()
        """
        return self.query.delete()
    
    def _apply_constraints(self):
        """Applique toutes les contraintes à la requête"""
        self.add_constraints(self.query)
        
        for constraint in self._constraints:
            constraint(self.query)

    def without_global_scopes(self):
        """Désactive les scopes globaux pour cette relation"""
        self._with_global_scopes = False
        return self

    def with_trashed(self):
        """Inclut les éléments soft-deleted"""
        self._with_trashed = True
        return self

    def without_constraints(self):
        """Désactive les contraintes de clés étrangères"""
        self._constraints = []
        return self

    def __getattr__(self, key: str) -> Any:
        """
        Délègue les attributs non trouvés au premier résultat de la relation.
        
        Example:
            # Au lieu de:
            post.author().first().name
            
            # On peut écrire:
            post.author().name
        """
        result = self.first()
        if result is None:
            raise AttributeError(f"Cannot access '{key}' on None result")
        return getattr(result, key) 