from typing import List, Union, Any, Dict

from .interfaces import FilterGroupInterface, LogicalOperator
from .filter_condition import FilterCondition

class FilterGroup(FilterGroupInterface):
    """
    Groupe de conditions de filtrage.
    
    Example:
        group = FilterGroup(LogicalOperator.AND)
        group.add(FilterCondition('age', '>=', 18))
        group.add(FilterCondition('status', '=', 'active'))
        
        # Groupe imbriqué
        subgroup = FilterGroup(LogicalOperator.OR)
        subgroup.add(FilterCondition('role', '=', 'admin'))
        subgroup.add(FilterCondition('role', '=', 'moderator'))
        group.add(subgroup)
    """
    
    def __init__(self, operator: LogicalOperator = LogicalOperator.AND):
        self.operator = operator
        self.conditions: List[Union[FilterCondition, 'FilterGroup']] = []
        
    def add(self, condition: Union[FilterCondition, 'FilterGroup']) -> 'FilterGroup':
        """Ajoute une condition ou un sous-groupe"""
        self.conditions.append(condition)
        return self
        
    def add_condition(self, field: str, operator: str, value: Any = None) -> 'FilterGroup':
        """
        Ajoute une nouvelle condition.
        
        Example:
            group.add_condition('age', '>=', 18)
        """
        self.add(FilterCondition(field, operator, value))
        return self
        
    def add_group(self, operator: LogicalOperator = LogicalOperator.AND) -> 'FilterGroup':
        """
        Crée et ajoute un nouveau sous-groupe.
        
        Example:
            subgroup = group.add_group(LogicalOperator.OR)
            subgroup.add_condition('role', '=', 'admin')
        """
        group = FilterGroup(operator)
        self.add(group)
        return group
        
    def to_dict(self) -> Dict[str, Any]:
        """Convertit le groupe en dictionnaire"""
        return {
            'operator': self.operator.value,
            'conditions': [condition.to_dict() for condition in self.conditions]
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FilterGroup':
        """Crée un groupe depuis un dictionnaire"""
        group = cls(LogicalOperator(data['operator']))
        
        for condition_data in data['conditions']:
            if 'operator' in condition_data:
                group.add(cls.from_dict(condition_data))
            else:
                group.add(FilterCondition.from_dict(condition_data))
                
        return group 