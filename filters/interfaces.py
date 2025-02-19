from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union, TypeVar
from enum import Enum

class LogicalOperator(Enum):
    """Opérateurs logiques pour grouper les conditions"""
    AND = 'AND'
    OR = 'OR'

FilterType = TypeVar('FilterType', bound='FilterInterface')
GroupType = TypeVar('GroupType', bound='FilterGroupInterface')
ConditionType = TypeVar('ConditionType', bound='FilterConditionInterface')

class FilterConditionInterface(ABC):
    """Interface pour les conditions de filtrage"""
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        pass
        
    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FilterConditionInterface':
        pass

class FilterGroupInterface(ABC):
    """Interface pour les groupes de conditions"""
    
    @abstractmethod
    def add(self, condition: Union[FilterConditionInterface, 'FilterGroupInterface']) -> 'FilterGroupInterface':
        pass
        
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        pass
        
    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FilterGroupInterface':
        pass 