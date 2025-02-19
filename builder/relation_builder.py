from typing import Any, Dict, List, Optional, Union, Type, TypeVar, Callable
from sqlalchemy import select, and_, or_, desc, asc
from sqlalchemy.sql import Select
from sqlalchemy.orm import joinedload, contains_eager

from ..types import ModelType, FilterValue, FilterOperator
from ..filters import Filter, FilterGroup, FilterCondition, Operator
from ..exceptions import InvalidQueryException, RelationNotLoadedException
from .query_builder import QueryBuilder

T = TypeVar('T', bound=ModelType)

class RelationBuilder(QueryBuilder):
    """
    Builder spécialisé pour la construction de requêtes de relations.
    
    Example:
        # Relation simple
        posts = user.posts()\
            .where('is_published', True)\
            .order_by('created_at', 'desc')\
            .get()
            
        # Avec relations imbriquées
        posts = user.posts()\
            .with_('comments', lambda q:
                q.where('is_approved', True)\
                 .with_('author')
            )\
            .where('views', '>', 1000)\
            .get()
            
        # Requêtes sur la table pivot
        roles = user.roles()\
            .where_pivot('expires_at', '>', 'now()')\
            .order_by_pivot('created_at', 'desc')\
            .get()
    """
    
    def __init__(
        self,
        parent: ModelType,
        related: Type[ModelType],
        table: Optional[str] = None,
        foreign_key: Optional[str] = None,
        local_key: str = 'id'
    ):
        """
        Initialise le builder de relation.
        
        Args:
            parent: Modèle parent
            related: Classe du modèle lié
            table: Nom de la table pivot (pour many-to-many)
            foreign_key: Clé étrangère
            local_key: Clé locale
        """
        super().__init__(related)
        self.parent = parent
        self.table = table
        self.foreign_key = foreign_key
        self.local_key = local_key
        self._pivot_columns: List[str] = []
        self._pivot_wheres: List[FilterCondition] = []
        self._pivot_orders: List[Dict[str, str]] = []
        
    def with_pivot(self, *columns: str) -> 'RelationBuilder[T]':
        """
        Spécifie les colonnes à récupérer de la table pivot.
        
        Example:
            roles = user.roles()\
                .with_pivot('expires_at', 'created_at')\
                .get()
        """
        self._pivot_columns.extend(columns)
        return self
        
    def where_pivot(
        self,
        column: str,
        operator: Union[str, Operator],
        value: Any = None
    ) -> 'RelationBuilder[T]':
        """
        Ajoute une condition WHERE sur la table pivot.
        
        Example:
            roles = user.roles()\
                .where_pivot('expires_at', '>', 'now()')\
                .get()
        """
        if isinstance(operator, Operator):
            operator = operator.value
            
        self._pivot_wheres.append(FilterCondition(column, operator, value))
        return self
        
    def order_by_pivot(
        self,
        column: str,
        direction: str = 'asc'
    ) -> 'RelationBuilder[T]':
        """
        Ajoute un ORDER BY sur la table pivot.
        
        Example:
            roles = user.roles()\
                .order_by_pivot('created_at', 'desc')\
                .get()
        """
        direction = direction.lower()
        if direction not in ('asc', 'desc'):
            raise InvalidQueryException(f"Direction invalide: {direction}")
            
        self._pivot_orders.append({
            'column': column,
            'direction': direction
        })
        return self
        
    def _build_query(self) -> Select:
        """Construit la requête SQL finale avec les jointures."""
        query = super()._build_query()
        
        # Ajoute la jointure de base
        if self.table:  # Many-to-many
            query = self._add_pivot_join(query)
        else:  # One-to-many ou One-to-one
            query = query.join(
                self.model,
                getattr(self.model, self.foreign_key) == getattr(self.parent, self.local_key)
            )
            
        # Ajoute les conditions sur la table pivot
        if self._pivot_wheres:
            for condition in self._pivot_wheres:
                query = query.where(self._build_pivot_condition(condition))
                
        # Ajoute les ORDER BY sur la table pivot
        for order in self._pivot_orders:
            column = getattr(self.table, order['column'])
            query = query.order_by(
                desc(column) if order['direction'] == 'desc' else asc(column)
            )
            
        return query
        
    def _add_pivot_join(self, query: Select) -> Select:
        """Ajoute la jointure pour une relation many-to-many."""
        query = query.join(
            self.table,
            and_(
                getattr(self.table, self.foreign_key) == getattr(self.parent, self.local_key),
                getattr(self.model, 'id') == getattr(self.table, self.related_key)
            )
        )
        
        # Ajoute les colonnes de la table pivot
        if self._pivot_columns:
            for column in self._pivot_columns:
                query = query.add_columns(
                    getattr(self.table, column).label(f"pivot_{column}")
                )
                
        return query
        
    def _build_pivot_condition(self, condition: FilterCondition) -> Any:
        """Construit une condition SQL pour la table pivot."""
        column = getattr(self.table, condition.field)
        
        if condition.operator == Operator.NULL.value:
            return column.is_(None)
            
        if condition.operator == Operator.NOT_NULL.value:
            return column.isnot(None)
            
        if condition.operator == Operator.IN.value:
            return column.in_(condition.value)
            
        if condition.operator == Operator.NOT_IN.value:
            return ~column.in_(condition.value)
            
        if condition.operator == Operator.BETWEEN.value:
            return column.between(*condition.value)
            
        if condition.operator == Operator.NOT_BETWEEN.value:
            return ~column.between(*condition.value)
            
        if condition.operator == Operator.LIKE.value:
            return column.like(condition.value)
            
        if condition.operator == Operator.ILIKE.value:
            return column.ilike(condition.value)
            
        return column.op(condition.operator)(condition.value) 