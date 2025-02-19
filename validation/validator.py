from typing import Any, Dict, List, Optional, Type, Union
from .interfaces import ValidatorInterface, RuleInterface

class ValidationError(Exception):
    def __init__(self, errors: Dict[str, List[str]]):
        self.errors = errors
        super().__init__(str(errors))

class Validator(ValidatorInterface):
    """
    Validateur principal avec support des règles personnalisées.
    
    Example:
        validator = Validator(
            data={'email': 'test@example.com'},
            rules={'email': [Required(), Email()]}
        )
        
        if validator.fails():
            print(validator.errors())
        else:
            data = validator.validated()
    """
    
    def __init__(
        self,
        data: Dict[str, Any],
        rules: Dict[str, List[RuleInterface]]
    ):
        self.data = data
        self.rules = rules
        self._errors: Dict[str, List[str]] = {}
        
    def validate(self) -> bool:
        """Valide les données selon les règles définies"""
        self._errors = {}
        
        for attribute, rules in self.rules.items():
            value = self.data.get(attribute)
            
            for rule in rules:
                result = rule.validate(attribute, value)
                if result is not True:
                    if attribute not in self._errors:
                        self._errors[attribute] = []
                    self._errors[attribute].append(str(result))
                    
        return len(self._errors) == 0
        
    def fails(self) -> bool:
        """Vérifie si la validation a échoué"""
        return not self.validate()
        
    def errors(self) -> Dict[str, List[str]]:
        """Retourne les erreurs de validation"""
        return self._errors
        
    def validated(self) -> Dict[str, Any]:
        """Retourne les données validées ou lève une exception"""
        if self.fails():
            raise ValidationError(self.errors())
        return self.data 