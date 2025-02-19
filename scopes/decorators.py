from typing import Callable, Any
from functools import wraps

from ..builder import QueryBuilder

def scope(func: Callable[[QueryBuilder], QueryBuilder]) -> Callable:
    """
    Décorateur pour définir un scope local.
    
    Example:
        @scope
        def published(query):
            return query.where('is_published', True)
    """
    @wraps(func)
    def wrapper(cls, query: QueryBuilder) -> QueryBuilder:
        return func(query)
    return wrapper 