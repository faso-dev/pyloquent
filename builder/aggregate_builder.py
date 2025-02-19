from typing import Any, Dict, List, Optional, Union, Type, TypeVar, Callable
from sqlalchemy import func, and_, or_, desc, asc, select
from sqlalchemy.sql import Select
from sqlalchemy.sql.expression import Function

from .interfaces import BuilderInterface
from ..types import ModelType, FilterValue, FilterOperator
from ..filters import Filter, FilterGroup, FilterCondition, Operator
from ..exceptions import InvalidQueryException

T = TypeVar('T', bound=ModelType)

class AggregateBuilder(BuilderInterface):
    """
    Builder spécialisé pour les opérations d'agrégation complexes.
    
    Example:
        # Agrégations simples
        stats = Order.aggregate()\
            .count('id', 'total_orders')\
            .sum('amount', 'total_amount')\
            .avg('amount', 'average_amount')\
            .group_by('status')\
            .get()
            
        # Avec conditions
        stats = User.aggregate()\
            .count('id', 'total_users')\
            .when(
                include_inactive,
                lambda q: q.where('status', '=', 'inactive')
            )\
            .having('total_users', '>', 10)\
            .get()
            
        # Agrégations imbriquées
        stats = Post.aggregate()\
            .count('id', 'posts_count')\
            .max('views', 'max_views')\
            .group_by('author_id')\
            .having('posts_count', '>', 5)\
            .order_by('max_views', 'desc')\
            .get()
    """
    
    def __init__(self, model: Type[ModelType]):
        super().__init__(model)
        self._aggregates: List[Dict[str, Any]] = []
        self._groups: List[str] = []
        self._filters: List[FilterCondition] = []
        self._havings: List[Dict[str, Any]] = []
        self._orders: List[Dict[str, str]] = []
        self._limit: Optional[int] = None
        self._offset: Optional[int] = None
        
    def select(self, *columns: str) -> 'AggregateBuilder':
        """
        Sélectionne des colonnes supplémentaires.
        
        Example:
            query.select('status', 'category')\
                .count('id', 'total')
        """
        for column in columns:
            self._aggregates.append({
                'type': 'column',
                'column': column,
                'alias': column
            })
        return self
        
    def count(self, column: str, alias: Optional[str] = None) -> 'AggregateBuilder':
        """
        Ajoute un COUNT.
        
        Example:
            query.count('id', 'total_users')
        """
        self._aggregates.append({
            'type': 'count',
            'column': column,
            'alias': alias or f"count_{column}"
        })
        return self
        
    def sum(self, column: str, alias: Optional[str] = None) -> 'AggregateBuilder':
        """
        Ajoute un SUM.
        
        Example:
            query.sum('amount', 'total_amount')
        """
        self._aggregates.append({
            'type': 'sum',
            'column': column,
            'alias': alias or f"sum_{column}"
        })
        return self
        
    def avg(self, column: str, alias: Optional[str] = None) -> 'AggregateBuilder':
        """
        Ajoute un AVG.
        
        Example:
            query.avg('rating', 'average_rating')
        """
        self._aggregates.append({
            'type': 'avg',
            'column': column,
            'alias': alias or f"avg_{column}"
        })
        return self
        
    def min(self, column: str, alias: Optional[str] = None) -> 'AggregateBuilder':
        """
        Ajoute un MIN.
        
        Example:
            query.min('price', 'lowest_price')
        """
        self._aggregates.append({
            'type': 'min',
            'column': column,
            'alias': alias or f"min_{column}"
        })
        return self
        
    def max(self, column: str, alias: Optional[str] = None) -> 'AggregateBuilder':
        """
        Ajoute un MAX.
        
        Example:
            query.max('views', 'most_views')
        """
        self._aggregates.append({
            'type': 'max',
            'column': column,
            'alias': alias or f"max_{column}"
        })
        return self
        
    def group_by(self, *columns: str) -> 'AggregateBuilder':
        """
        Ajoute un GROUP BY.
        
        Example:
            query.group_by('status', 'category')
        """
        self._groups.extend(columns)
        return self
        
    def having(
        self,
        column: str,
        operator: Union[str, Operator],
        value: Any
    ) -> 'AggregateBuilder':
        """
        Ajoute une condition HAVING.
        
        Example:
            query.having('count_id', '>', 10)
        """
        if isinstance(operator, Operator):
            operator = operator.value
            
        self._havings.append({
            'column': column,
            'operator': operator,
            'value': value
        })
        return self
        
    def order_by(self, column: str, direction: str = 'asc') -> 'AggregateBuilder':
        """
        Ajoute un ORDER BY.
        
        Example:
            query.order_by('total_amount', 'desc')
        """
        direction = direction.lower()
        if direction not in ('asc', 'desc'):
            raise InvalidQueryException(f"Direction invalide: {direction}")
            
        self._orders.append({
            'column': column,
            'direction': direction
        })
        return self

    def get(self) -> Dict[str, Any]:
        """
        Exécute la requête d'agrégation et retourne les résultats.
        
        Raises:
            InvalidQueryException: Si la requête est invalide
            
        Returns:
            Dict[str, Any]: Résultats des agrégations
        """
        if not self._aggregates:
            raise InvalidQueryException("No aggregates defined")
            
        query = self._build_query()
        result = query.first()
        
        return {
            agg['alias']: getattr(result, agg['alias'])
            for agg in self._aggregates
        }
    
    def _build_query(self):
        """Construit la requête SQL finale"""
        query = self._query
        
        # Ajoute les agrégats
        for agg in self._aggregates:
            column = getattr(self._query.model, agg['column'])
            match agg['type']:
                case 'count':
                    expr = func.count(column)
                case 'sum':
                    expr = func.sum(column)
                case 'avg':
                    expr = func.avg(column)
                case 'min':
                    expr = func.min(column)
                case 'max':
                    expr = func.max(column)
                case _:
                    raise InvalidQueryException(f"Invalid aggregate type: {agg['type']}")
                    
            query = query.add_columns(expr.label(agg['alias']))
            
        # Ajoute les groupements
        if self._groups:
            query = query.group_by(*self._groups)
            
        # Ajoute les conditions HAVING
        for having in self._havings:
            query = query.having(
                self._build_having_condition(having)
            )
            
        # Ajoute les conditions WHERE
        for filter in self._filters:
            query = query.where(
                self._build_filter_condition(filter)
            )
            
        # Ajoute les conditions ORDER BY
        for order in self._orders:
            query = query.order_by(
                getattr(getattr(self._query.model, order['column']), order['direction'])
            )
            
        # Ajoute les limites et les offsets
        if self._limit:
            query = query.limit(self._limit)
        if self._offset:
            query = query.offset(self._offset)
            
        return query 