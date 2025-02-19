from typing import Any, List, Dict, Optional, TypeVar, Union, Type, Callable
from sqlalchemy import select, func, and_, or_, desc, asc
from sqlalchemy.sql import Select
from sqlalchemy.orm import Query, joinedload

from .interfaces import BuilderInterface
from ..types import ModelType, FilterValue, FilterOperator
from ..exceptions.pyloquent_exception import ModelNotFoundException
from ..filters import Filter, FilterGroup, FilterCondition, Operator
from ..pagination import Paginator, LengthAwarePaginator, CursorPaginator

from libs.pyloquent.exceptions import InvalidQueryException

T = TypeVar('T', bound=ModelType)

class QueryBuilder(BuilderInterface):
    """
    Builder to build SQL queries fluently.
    
    Example:
        # Simple query
        users = User.query()\
            .where('age', '>=', 18)\
            .where('status', '=', 'active')\
            .order_by('created_at', 'desc')\
            .get()
            
        # With relations
        posts = Post.query()\
            .with_('author')\
            .with_('comments', lambda q:
                q.where('is_approved', True)\
                 .with_('author')
            )\
            .where('is_published', True)\
            .paginate()
            
        # Advanced queries
        users = User.query()\
            .where_has('posts', lambda q:
                q.where('views', '>', 1000)
            )\
            .where_doesnt_have('suspensions')\
            .order_by_desc('created_at')\
            .take(10)\
            .get()
    """
    
    def __init__(self, model: Type[ModelType]):
        super().__init__(model)
        self._query: Select = select(model)
        self._filters: List[FilterCondition] = []
        self._or_filters: List[FilterGroup] = []
        self._eager_loads: Dict[str, Optional[Callable]] = {}
        self._orders: List[Dict[str, str]] = []
        self._groups: List[str] = []
        self._limit: Optional[int] = None
        self._offset: Optional[int] = None
        self._cursor: Optional[Dict[str, Any]] = None
        self._after_load_callbacks: List[Callable] = []
        
    def select(self, *columns: str) -> 'QueryBuilder':
        """
        Specify the columns to select.
        
        Example:
            query.select('name', 'email')
        """
        self._query = select(*[getattr(self.model, col) for col in columns])
        return self
        
    def where(
        self,
        column: str,
        operator: Union[str, Operator] = Operator.EQUAL.value,
        value: Any = None
    ) -> 'QueryBuilder':
        """
        Add a WHERE condition.
        
        Example:
            query.where('age', '>=', 18)
            query.where('status', Operator.EQUAL, 'active')
        """
        if isinstance(operator, Operator):
            operator = operator.value
            
        self._filters.append(FilterCondition(column, operator, value))
        return self
        
    def or_where(
        self,
        column: str,
        operator: Union[str, Operator],
        value: Any = None
    ) -> 'QueryBuilder':
        """
        Add an OR WHERE condition.
        
        Example:
            query.or_where('age', Operator.EQUAL, 18)
        """
        group = FilterGroup()
        group.add_condition(column, operator, value)
        self._or_filters.append(group)
        return self
        
    def where_in(self, column: str, values: List[Any]) -> 'QueryBuilder':
        """
        Add a condition WHERE IN.
        
        Example:
            query.where_in('age', [20, 30])
        """
        return self.where(column, Operator.IN, values)
        
    def where_not_in(self, column: str, values: List[Any]) -> 'QueryBuilder':
        """
        Add a condition WHERE NOT IN.
        
        Example:
            query.where_not_in('age', [20, 30])
        """
        return self.where(column, Operator.NOT_IN, values)
        
    def where_null(self, column: str) -> 'QueryBuilder':
        """
        Add a condition WHERE IS NULL.
        
        Example:
            query.where_null('age')
        """
        return self.where(column, Operator.NULL)
        
    def where_not_null(self, column: str) -> 'QueryBuilder':
        """
        Add a condition WHERE IS NOT NULL.
        
        Example:
            query.where_not_null('age')
        """
        return self.where(column, Operator.NOT_NULL)
        
    def where_between(self, column: str, values: List[Any]) -> 'QueryBuilder':
        """
        Add a condition WHERE BETWEEN.
        
        Example:
            query.where_between('age', [20, 30])
        """
        return self.where(column, Operator.BETWEEN, values)
        
    def where_not_between(self, column: str, values: List[Any]) -> 'QueryBuilder':
        """
        Add a condition WHERE NOT BETWEEN.
        
        Example:
            query.where_not_between('age', [20, 30])
        """
        return self.where(column, Operator.NOT_BETWEEN, values)
        
    def where_like(self, column: str, pattern: str) -> 'QueryBuilder':
        """
        Add a condition WHERE LIKE.
        
        Example:
            query.where_like('name', '%John%')
        """
        return self.where(column, Operator.LIKE, pattern)
        
    def where_ilike(self, column: str, pattern: str) -> 'QueryBuilder':
        """
        Add a condition WHERE ILIKE.
        
        Example:
            query.where_ilike('name', '%John%')
        """
        return self.where(column, Operator.ILIKE, pattern)
        
    def where_has(
        self,
        relation: str,
        callback: Optional[Callable[['QueryBuilder'], None]] = None
    ) -> 'QueryBuilder':
        """
        Filter by the existence of a relation.
        
        Example:
            # Find users with posts with more than 1000 views
            User.query().where_has('posts', lambda q:
                q.where('views', '>', 1000)
            )
            
            # Find posts with at least one comment
            Post.query().where_has('comments')
        """
        # Retrieve the relation of the model
        if not hasattr(self.model, relation):
            raise InvalidQueryException(f"Relation {relation} not found on {self.model.__name__}")
        
        relation_obj = getattr(self.model, relation)()
        
        # Create a subquery for the relation
        subquery = relation_obj.get_query()
        
        # Apply additional constraints if provided
        if callback:
            callback(subquery)
        
        # Add the join condition
        subquery = subquery.where(
            relation_obj.get_foreign_key(),
            '=',
            getattr(self.model, relation_obj.get_local_key())
        )
        
        # Add the EXISTS condition to the main query
        self._query = self._query.where(subquery.exists())
        
        return self
        
    def where_doesnt_have(
        self,
        relation: str,
        callback: Optional[Callable[['QueryBuilder'], None]] = None
    ) -> 'QueryBuilder':
        """
        Filter by the absence of a relation.
        
        Example:
            # Find users who don't have posts
            User.query().where_doesnt_have('posts')
            
            # Find posts that don't have approved comments
            Post.query().where_doesnt_have('comments', lambda q:
                q.where('is_approved', True)
            )
        """
        # Retrieve the relation of the model
        if not hasattr(self.model, relation):
            raise InvalidQueryException(f"Relation {relation} not found on {self.model.__name__}")
        
        relation_obj = getattr(self.model, relation)()
        
        # Create a subquery for the relation
        subquery = relation_obj.get_query()
        
        # Apply additional constraints if provided
        if callback:
            callback(subquery)
        
        # Add the join condition
        subquery = subquery.where(
            relation_obj.get_foreign_key(),
            '=',
            getattr(self.model, relation_obj.get_local_key())
        )
        
        # Add the NOT EXISTS condition to the main query
        self._query = self._query.where(~subquery.exists())
        
        return self
        
    def with_(
        self,
        relation: str,
        callback: Optional[Callable[['QueryBuilder'], None]] = None
    ) -> 'QueryBuilder':
        """
        Load a relation eagerly.
        
        Example:
            query.with_('posts')
            query.with_('comments', lambda q:
                q.where('is_approved', True)
            )
        """
        self._eager_loads[relation] = callback
        
        # Automatically add the callback to mark the relation as loaded
        def mark_loaded(model):
            if not hasattr(model, '_loaded_relations'):
                model._loaded_relations = set()
            model._loaded_relations.add(relation)
        self.after_load(mark_loaded)
        
        return self
        
    def order_by(self, column: str, direction: str = 'asc') -> 'QueryBuilder':
        """
        Add an ORDER BY.
        
        Example:
            query.order_by('created_at', 'desc')
        """
        direction = direction.lower()
        if direction not in ('asc', 'desc'):
            raise InvalidQueryException(f"Invalid direction: {direction}")
            
        self._orders.append({'column': column, 'direction': direction})
        return self
        
    def order_by_desc(self, column: str) -> 'QueryBuilder':
        """Add a DESC ORDER BY."""
        return self.order_by(column, 'desc')
        
    def group_by(self, *columns: str) -> 'QueryBuilder':
        """
        Add a GROUP BY.
        
        Example:
            query.group_by('status', 'role')
        """
        self._groups.extend(columns)
        return self
        
    def take(self, limit: int) -> 'QueryBuilder':
        """
        Limit the number of results.
        
        Example:
            query.take(5)  # LIMIT 5
        """
        if limit < 0:
            raise InvalidQueryException("The limit must be positive")
        self._limit = limit
        return self
        
    def skip(self, offset: int) -> 'QueryBuilder':
        """
        Skip a number of results.
        
        Example:
            query.skip(10)  # OFFSET 10
        """
        if offset < 0:
            raise InvalidQueryException("The offset must be positive")
        self._offset = offset
        return self
        
    def paginate(
        self,
        page: int = 1,
        per_page: int = 15,
        path: Optional[str] = None,
        query_params: Optional[Dict[str, Any]] = None
    ) -> LengthAwarePaginator[T]:
        """
        Paginate the results with total number.
        
        Example:
            result = query.paginate(page=2, per_page=15)
            
            # With path for links
            result = query.paginate(
                page=2,
                path='/api/users',
                query_params={'status': 'active'}
            )
        """
        if page < 1:
            raise InvalidQueryException("The page number must be positive")
            
        total = self.count()
        items = self.skip((page - 1) * per_page).take(per_page).get()
        
        return LengthAwarePaginator(
            items=items,
            total=total,
            page=page,
            per_page=per_page,
            path=path,
            query_params=query_params
        )
        
    def cursor_paginate(
        self,
        cursor_field: str = 'id',
        limit: int = 15,
        after: Any = None,
        before: Any = None
    ) -> CursorPaginator[T]:
        """
        Paginate the results with cursor.
        
        Example:
            # First page
            result = query.cursor_paginate(limit=20)
            
            # Next page
            next_page = query.cursor_paginate(
                after=result.next_cursor,
                limit=20
            )
        """
        self._cursor = {
            'field': cursor_field,
            'after': after,
            'before': before
        }
        
        self.take(limit + 1)  # +1 to check if there is a next page
        
        if after:
            self.where(cursor_field, '>', after)
        elif before:
            self.where(cursor_field, '<', before)
            
        items = self.get()
        has_more = len(items) > limit
        
        if has_more:
            items = items[:limit]
            
        return CursorPaginator(
            items=items,
            has_more=has_more,
            cursor_field=cursor_field,
            limit=limit,
            next_cursor=items[-1].get_attribute(cursor_field) if has_more else None,
            previous_cursor=items[0].get_attribute(cursor_field) if items else None
        )
        
    def get(self) -> List[T]:
        """
        Execute the query and return the results.
        
        Example:
            users = query.where('active', True).get()
        """
        results = self._execute_query()
        
        # Execute the after_load callbacks
        for result in results:
            for callback in self._after_load_callbacks:
                callback(result)
                
        return results
        
    def first(self) -> Optional[T]:
        """
        Return the first result.
        
        Example:
            user = query.where('email', email).first()
        """
        self.take(1)
        results = self.get()
        return results[0] if results else None
        
    def find(self, id: Any) -> Optional[T]:
        """
        Find a model by its ID.
        
        Example:
            user = User.query().find(5)
        """
        return self.where('id', Operator.EQUAL, id).first()
        
    def find_or_fail(self, id: Any) -> T:
        """
        Find a model by its ID or raise a ModelNotFoundException.
        
        Example:
            user = User.query().find_or_fail(5)
            # Raise ModelNotFoundException if not found
        """
        result = self.find(id)
        if result is None:
            raise ModelNotFoundException(self.model.__name__, id)
        return result
        
    def count(self) -> int:
        """
        Count the total number of results.
        
        Example:
            count = query.where('active', True).count()
        """
        # Create a subquery with the current filters
        subquery = self._build_query()
        
        # Create a new COUNT query on the subquery
        count_query = select(func.count()).select_from(subquery)
        
        # Execute the query
        session = self.model.get_session()
        result = session.execute(count_query).scalar()
        
        return result or 0
        
    def exists(self) -> bool:
        """
        Check if the query returns results.
        
        Example:
            if query.where('email', email).exists():
                print("Email already used")
        """
        # Optimise en limitant à 1 résultat
        return self.take(1).get() != []
        
    def _execute_query(self, query=None) -> List[T]:
        """
        Execute the SQL query.
        
        Args:
            query: Optional SQL query. If not provided, use _build_query()
        """
        if query is None:
            query = self._build_query()
        
        session = self.model.get_session()
        return session.execute(query).scalars().all()
        
    def _build_query(self) -> Select:
        """Build the SQL query with all clauses."""
        query = self._query
        
        # Add WHERE conditions
        if self._filters:
            conditions = [self._build_condition(f) for f in self._filters]
            query = query.where(and_(*conditions))
            
        # Add OR WHERE conditions
        if self._or_filters:
            or_conditions = [
                and_(*[self._build_condition(c) for c in group.conditions])
                for group in self._or_filters
            ]
            query = query.where(or_(*or_conditions))
            
        # Add ORDER BY
        for order in self._orders:
            column = getattr(self.model, order['column'])
            query = query.order_by(
                desc(column) if order['direction'] == 'desc' else asc(column)
            )
            
        # Add GROUP BY
        if self._groups:
            query = query.group_by(*[getattr(self.model, col) for col in self._groups])
            
        # Add LIMIT/OFFSET
        if self._limit is not None:
            query = query.limit(self._limit)
        if self._offset is not None:
            query = query.offset(self._offset)
            
        return query 

    def _build_condition(self, condition: FilterCondition) -> Any:
        """
        Build an SQL condition from a FilterCondition.
        
        Args:
            condition: The condition to build
            
        Returns:
            An SQLAlchemy expression
        """
        column = getattr(self.model, condition.field)
        
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
        
    def _add_eager_loads(self, query: Select) -> Select:
        """
        Add eager loads of relations.
        
        Args:
            query: The query to modify
            
        Returns:
            The modified query
        """
        for relation, callback in self._eager_loads.items():
            loader = joinedload(getattr(self.model, relation))
            
            if callback:
                subquery = QueryBuilder(self.model)
                callback(subquery)
                loader = loader.options(*subquery._eager_loads)
                
            query = query.options(loader)
            
        return query
        
    # Aggregation methods
    
    def max(self, column: str) -> Any:
        """
        Return the maximum value of a column.
        
        Example:
            max_price = Product.query().max('price')
        """
        return self.select(func.max(getattr(self.model, column))).scalar()
        
    def min(self, column: str) -> Any:
        """
        Return the minimum value of a column.
        
        Example:
            min_age = User.query().min('age')
        """
        return self.select(func.min(getattr(self.model, column))).scalar()
        
    def sum(self, column: str) -> Any:
        """
        Return the sum of a column.
        
        Example:
            total_sales = Order.query().sum('amount')
        """
        return self.select(func.sum(getattr(self.model, column))).scalar()
        
    def avg(self, column: str) -> float:
        """
        Return the average of a column.
        
        Example:
            avg_rating = Product.query().avg('rating')
        """
        return self.select(func.avg(getattr(self.model, column))).scalar()
        
    def chunk(self, count: int, callback: Callable[[List[T]], None]) -> bool:
        """
        Process results in chunks.
        
        Args:
            count: The size of the chunk
            callback: Function to call for each chunk
            
        Example:
            User.query().chunk(100, lambda users:
                for user in users:
                    # Process by chunk
                    process_user(user)
            )
        """
        page = 1
        
        while True:
            results = self.skip((page - 1) * count).take(count).get()
            
            if not results:
                break
                
            callback(results)
            
            if len(results) < count:
                break
                
            page += 1
            
        return True
        
    def each(self, callback: Callable[[T], None], count: int = 100) -> bool:
        """
        Process each result individually in chunks.
        
        Args:
            callback: Function to call for each element
            count: The size of the chunk
            
        Example:
            User.query().each(lambda user:
                # Process individually
                process_user(user)
            )
        """
        return self.chunk(count, lambda results: [callback(result) for result in results])
        
    def update(self, values: Dict[str, Any]) -> int:
        """
        Update the records that match the query.
        
        Example:
            # Update the status of all inactive users
            User.query()\
                .where('last_login', '<', '2023-01-01')\
                .update({'status': 'inactive'})
        """
        query = self._build_query()
        result = self.model.session.execute(
            query.update().values(**values)
        )
        self.model.session.commit()
        return result.rowcount
        
    def delete(self) -> int:
        """
        Delete the records that match the query.
        
        Example:
            # Delete all unpublished posts
            Post.query()\
                .where('status', '=', 'draft')\
                .where('created_at', '<', '2023-01-01')\
                .delete()
        """
        query = self._build_query()
        result = self.model.session.execute(query.delete())
        self.model.session.commit()
        return result.rowcount
        
    def force_delete(self) -> int:
        """
        Delete the records definitively (ignore the soft delete).
        
        Example:
            # Delete definitively the users marked as deleted
            User.query()\
                .only_trashed()\
                .where('deleted_at', '<', '2022-01-01')\
                .force_delete()
        """
        self._ignore_soft_delete = True
        return self.delete()
        
    # Méthodes de gestion des soft deletes
    
    def with_trashed(self) -> 'QueryBuilder':
        """
        Include the soft-deleted records in the query.
        
        Example:
            users = User.query().with_trashed().get()
        """
        self._with_trashed = True
        return self
        
    def only_trashed(self) -> 'QueryBuilder':
        """
        Return only the soft-deleted records.
        
        Example:
            deleted_users = User.query().only_trashed().get()
        """
        self._only_trashed = True
        return self
        
    def restore(self) -> int:
        """
        Restore the soft-deleted records.
        
        Example:
            # Restore the recently deleted users
            User.query()\
                .only_trashed()\
                .where('deleted_at', '>', '2023-01-01')\
                .restore()
        """
        return self.update({self.model.DELETED_AT_COLUMN: None})
        
    # Méthodes de gestion des scopes
    
    def with_global_scope(self, scope: 'Scope') -> 'QueryBuilder':
        """
        Add a global scope to the query.
        
        Example:
            query.with_global_scope(ActiveScope())
        """
        scope.apply(self, self.model)
        return self
        
    def without_global_scope(self, scope: Union[Type['Scope'], 'Scope']) -> 'QueryBuilder':
        """
        Disable a global scope for this query.
        
        Example:
            query.without_global_scope(SoftDeleteScope)
        """
        self._without_scopes.append(scope)
        return self
        
    def without_global_scopes(self) -> 'QueryBuilder':
        """
        Disable all global scopes for this query.
        
        Example:
            query.without_global_scopes().get()
        """
        self._without_scopes = list(self.model.get_global_scopes().values())
        return self
        
    # Méthodes utilitaires
    
    def clone(self) -> 'QueryBuilder':
        """
        Create a copy of the current query.
        
        Example:
            new_query = query.clone()
        """
        clone = QueryBuilder(self.model)
        clone._query = self._query
        clone._filters = self._filters.copy()
        clone._or_filters = self._or_filters.copy()
        clone._eager_loads = self._eager_loads.copy()
        clone._orders = self._orders.copy()
        clone._groups = self._groups.copy()
        clone._limit = self._limit
        clone._offset = self._offset
        clone._cursor = self._cursor.copy() if self._cursor else None
        clone._after_load_callbacks = self._after_load_callbacks.copy()
        return clone
        
    def tap(self, callback: Callable[['QueryBuilder'], None]) -> 'QueryBuilder':
        """
        Execute a function on the query and return the query.
        
        Example:
            query.tap(lambda q: print(q._build_query()))
        """
        callback(self)
        return self
        
    def when(
        self,
        condition: bool,
        true_callback: Callable[['QueryBuilder'], None],
        false_callback: Optional[Callable[['QueryBuilder'], None]] = None
    ) -> 'QueryBuilder':
        """
        Apply conditionally modifications to the query.
        
        Example:
            query.when(
                user.is_admin,
                lambda q: q.with_trashed(),
                lambda q: q.where('is_public', True)
            )
        """
        if condition:
            true_callback(self)
        elif false_callback:
            false_callback(self)
            
        return self
        
    def after_load(self, callback: Callable) -> 'QueryBuilder':
        """Add a callback to execute after loading"""
        self._after_load_callbacks.append(callback)
        return self 