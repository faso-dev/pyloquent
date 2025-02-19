from typing import Any, Dict, List, Optional, Union, Callable
from dataclasses import dataclass, field

from .interfaces import LogicalOperator
from .operators import Operator
from .filter_condition import FilterCondition
from .filter_group import FilterGroup

@dataclass
class Filter:
    """
    Classe principale pour construire et appliquer des filtres.
    
    Example:
        # Filtre simple
        filter = Filter()\
            .where('age', '>=', 18)\
            .where('status', '=', 'active')
            
        # Avec groupe OR
        filter.or_where(lambda group:
            group.where('role', '=', 'admin')
                .where('role', '=', 'moderator')
        )
        
        # Recherche insensible à la casse
        filter.where('name', 'ILIKE', '%john%')
        
        # Filtres avancés
        filter.where_in('status', ['pending', 'active'])\
              .where_null('deleted_at')\
              .where_between('created_at', ['2023-01-01', '2023-12-31'])
    """
    
    root_group: FilterGroup = field(default_factory=lambda: FilterGroup(LogicalOperator.AND))
    current_group: FilterGroup = field(init=False)
    
    def __post_init__(self):
        self.current_group = self.root_group
    
    def where(
        self,
        field: str,
        operator: Union[str, Operator],
        value: Any = None
    ) -> 'Filter':
        """
        Ajoute une condition WHERE.
        
        Args:
            field: Nom du champ
            operator: Opérateur de comparaison
            value: Valeur à comparer
            
        Example:
            filter.where('age', '>=', 18)
            filter.where('status', Operator.EQUAL, 'active')
        """
        if isinstance(operator, Operator):
            operator = operator.value
            
        self.current_group.add_condition(field, operator, value)
        return self
    
    def or_where(
        self,
        field_or_callback: Union[str, Callable[[FilterGroup], None]],
        operator: Optional[Union[str, Operator]] = None,
        value: Any = None
    ) -> 'Filter':
        """
        Ajoute une condition OR WHERE.
        
        Example:
            # Condition simple
            filter.or_where('role', '=', 'admin')
            
            # Groupe de conditions
            filter.or_where(lambda group:
                group.where('role', '=', 'admin')
                    .where('is_super', '=', True)
            )
        """
        if callable(field_or_callback):
            group = self.root_group.add_group(LogicalOperator.OR)
            field_or_callback(group)
            return self
            
        group = FilterGroup(LogicalOperator.OR)
        group.add_condition(field_or_callback, operator, value)
        self.root_group.add(group)
        return self
    
    def where_in(self, field: str, values: List[Any]) -> 'Filter':
        """Ajoute une condition WHERE IN."""
        return self.where(field, Operator.IN, values)
    
    def where_not_in(self, field: str, values: List[Any]) -> 'Filter':
        """Ajoute une condition WHERE NOT IN."""
        return self.where(field, Operator.NOT_IN, values)
    
    def where_null(self, field: str) -> 'Filter':
        """Ajoute une condition WHERE IS NULL."""
        return self.where(field, Operator.NULL)
    
    def where_not_null(self, field: str) -> 'Filter':
        """Ajoute une condition WHERE IS NOT NULL."""
        return self.where(field, Operator.NOT_NULL)
    
    def where_between(self, field: str, values: List[Any]) -> 'Filter':
        """Ajoute une condition WHERE BETWEEN."""
        if len(values) != 2:
            raise ValueError("La méthode where_between nécessite exactement 2 valeurs")
        return self.where(field, Operator.BETWEEN, values)
    
    def where_not_between(self, field: str, values: List[Any]) -> 'Filter':
        """Ajoute une condition WHERE NOT BETWEEN."""
        if len(values) != 2:
            raise ValueError("La méthode where_not_between nécessite exactement 2 valeurs")
        return self.where(field, Operator.NOT_BETWEEN, values)
    
    def where_like(self, field: str, pattern: str) -> 'Filter':
        """Ajoute une condition WHERE LIKE."""
        return self.where(field, Operator.LIKE, pattern)
    
    def where_ilike(self, field: str, pattern: str) -> 'Filter':
        """Ajoute une condition WHERE ILIKE (insensible à la casse)."""
        return self.where(field, Operator.ILIKE, pattern)
    
    def group(self, callback: Callable[[FilterGroup], None]) -> 'Filter':
        """
        Crée un nouveau groupe de conditions.
        
        Example:
            filter.group(lambda group:
                group.where('status', '=', 'active')
                     .or_where('status', '=', 'pending')
            )
        """
        group = self.root_group.add_group(LogicalOperator.AND)
        callback(group)
        return self
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit le filtre en dictionnaire."""
        return self.root_group.to_dict()
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Filter':
        """Crée un filtre depuis un dictionnaire."""
        filter = cls()
        filter.root_group = FilterGroup.from_dict(data)
        return filter 