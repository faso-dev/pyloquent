from typing import Any, List, Type, TypeVar, Dict, Optional
from libs.pyloquent.relations.relation import Relation
from ..types import ModelType
T = TypeVar('T', bound=ModelType)

class ManyToMany(Relation[T]):
    """
    Implémente une relation many-to-many.
    
    Example:
        class User(Model):
            def roles(self):
                return self.many_to_many(Role, 'role_user', 'user_id', 'role_id')
                
        class Role(Model):
            def users(self):
                return self.many_to_many(User, 'role_user', 'role_id', 'user_id')
                
        # Utilisation
        user = User.find(1)
        
        # Récupérer les rôles
        roles = user.roles().get()
        
        # Attacher des rôles
        user.roles().attach([1, 2, 3])
        
        # Attacher avec des données pivot
        user.roles().attach([
            1 => ['expires_at' => '2024-01-01'],
            2 => ['expires_at' => '2024-02-01']
        ])
        
        # Détacher
        user.roles().detach([1, 2])
        
        # Synchroniser
        user.roles().sync([1, 2, 3])
        
        # Requêtes avec conditions sur la table pivot
        admins = user.roles()\
            .where_pivot('is_active', True)\
            .where('name', 'admin')\
            .get()
    """
    
    def __init__(
        self,
        parent: Any,
        related: Type[T],
        table: str,
        foreign_pivot_key: str,
        related_pivot_key: str,
        parent_key: str = 'id',
        related_key: str = 'id',
        relation_name: str = None
    ):
        super().__init__(parent, related)
        self.table = table
        self.foreign_pivot_key = foreign_pivot_key
        self.related_pivot_key = related_pivot_key
        self.parent_key = parent_key
        self.related_key = related_key
        self.relation_name = relation_name or related.__name__.lower()
        self._pivot_columns = []
        
    def with_pivot(self, *columns: str) -> 'ManyToMany[T]':
        """
        Spécifie les colonnes à récupérer de la table pivot.
        
        Example:
            roles = user.roles()\
                .with_pivot('expires_at', 'created_at')\
                .get()
                
            role = roles[0]
            expires_at = role.pivot.expires_at
        """
        self._pivot_columns.extend(columns)
        return self
        
    def attach(self, ids: Dict[Any, Dict] | List[Any], attributes: Dict = None) -> None:
        """
        Attache des modèles à la relation.
        
        Args:
            ids: IDs à attacher avec données pivot optionnelles
            attributes: Attributs par défaut pour tous les enregistrements
            
        Example:
            # Simple
            user.roles().attach([1, 2, 3])
            
            # Avec données pivot
            user.roles().attach({
                1: {'expires_at': '2024-01-01'},
                2: {'expires_at': '2024-02-01'}
            })
        """
        records = self._format_attach_records(ids, attributes)
        self.db.table(self.table).insert(records)
        
    def detach(self, ids: List[Any] = None) -> int:
        """
        Détache des modèles de la relation.
        
        Example:
            # Détache spécifique
            user.roles().detach([1, 2])
            
            # Détache tout
            user.roles().detach()
        """
        query = self.db.table(self.table)\
            .where(self.foreign_pivot_key, self.parent.get_key())
            
        if ids is not None:
            query.where_in(self.related_pivot_key, ids)
            
        return query.delete()
        
    def sync(self, ids: Dict[Any, Dict] | List[Any], attributes: Dict = None) -> None:
        """
        Synchronise la relation avec une liste d'IDs.
        
        Example:
            # Simple sync
            user.roles().sync([1, 2, 3])
            
            # Avec données pivot
            user.roles().sync({
                1: {'expires_at': '2024-01-01'},
                2: {'expires_at': '2024-02-01'}
            })
        """
        current = self.current_pivot_ids()
        
        detach = current - set(self._get_ids(ids))
        attach = set(self._get_ids(ids)) - current
        
        if detach:
            self.detach(list(detach))
            
        if attach:
            self.attach(
                {id_: ids[id_] for id_ in attach}
                if isinstance(ids, dict)
                else list(attach),
                attributes
            ) 