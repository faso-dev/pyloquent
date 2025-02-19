from typing import Any, Dict
from dataclasses import dataclass

from .interfaces import FilterConditionInterface
from .operators import Operator

@dataclass
class FilterCondition(FilterConditionInterface):
    """
    Représente une condition de filtrage individuelle.
    
    Example:
        # Forme complète
        condition = FilterCondition('age', '>=', 18)
        condition = FilterCondition('status', 'IN', ['active', 'pending'])
        
        # Forme courte (utilise EQUAL par défaut)
        condition = FilterCondition('is_active', True)
        condition = FilterCondition('status', 'active')
    """
    field: str
    operator: str = Operator.EQUAL.value
    value: Any = None
    
    def __post_init__(self):
        """Validation après initialisation"""
        # Si value n'est pas fourni et operator n'est pas un opérateur valide,
        # on considère que operator est en fait la valeur
        if self.value is None and not Operator.validate(self.operator):
            self.value = self.operator
            self.operator = Operator.EQUAL.value
            
        # Maintenant on valide l'opérateur
        if not Operator.validate(self.operator):
            raise ValueError(f"Opérateur invalide: {self.operator}")
            
        if Operator.requires_value(self.operator) and self.value is None:
            raise ValueError(f"L'opérateur {self.operator} nécessite une valeur")
            
        if Operator.requires_array(self.operator):
            if not isinstance(self.value, (list, tuple)):
                raise ValueError(f"L'opérateur {self.operator} nécessite un tableau de valeurs")
                
    def to_dict(self) -> Dict[str, Any]:
        """Convertit la condition en dictionnaire"""
        return {
            'field': self.field,
            'operator': self.operator,
            'value': self.value
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FilterCondition':
        """Crée une condition depuis un dictionnaire"""
        return cls(
            field=data['field'],
            operator=data['operator'],
            value=data.get('value')
        ) 