from typing import Dict, List
from .base import ValidationException

class ValidationError(ValidationException):
    """Levée quand la validation échoue"""
    
    def __init__(self, errors: Dict[str, List[str]]):
        self.errors = errors
        super().__init__(str(errors))

class RuleValidationError(ValidationException):
    """Levée quand une règle de validation est invalide"""
    pass

class InvalidRuleException(ValidationException):
    """Levée quand une règle n'existe pas"""
    pass 