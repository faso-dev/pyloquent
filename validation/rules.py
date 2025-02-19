from typing import Any, Union, Pattern, List
import re
from datetime import datetime

from .interfaces import RuleInterface

class Rule(RuleInterface):
    """Classe de base pour les règles de validation"""
    
    def __init__(self, message: str = None):
        self._message = message
        
    def message(self, attribute: str, value: Any) -> str:
        return self._message or self.default_message(attribute, value)
        
    def default_message(self, attribute: str, value: Any) -> str:
        """Message d'erreur par défaut"""
        return f"The {attribute} is invalid"

class Required(Rule):
    def validate(self, attribute: str, value: Any) -> Union[bool, str]:
        if value is None or (isinstance(value, str) and not value.strip()):
            return self.message(attribute, value)
        return True
        
    def default_message(self, attribute: str, value: Any) -> str:
        return f"The {attribute} field is required"

class Email(Rule):
    def validate(self, attribute: str, value: Any) -> Union[bool, str]:
        if not value:
            return True
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, str(value)):
            return self.message(attribute, value)
        return True
        
    def default_message(self, attribute: str, value: Any) -> str:
        return f"The {attribute} must be a valid email address"

class MinLength(Rule):
    def __init__(self, min_length: int, message: str = None):
        super().__init__(message)
        self.min_length = min_length
        
    def validate(self, attribute: str, value: Any) -> Union[bool, str]:
        if not value:
            return True
        if len(str(value)) < self.min_length:
            return self.message(attribute, value)
        return True
        
    def default_message(self, attribute: str, value: Any) -> str:
        return f"The {attribute} must be at least {self.min_length} characters"

class MaxLength(Rule):
    def __init__(self, max_length: int, message: str = None):
        super().__init__(message)
        self.max_length = max_length
        
    def validate(self, attribute: str, value: Any) -> Union[bool, str]:
        if not value:
            return True
        if len(str(value)) > self.max_length:
            return self.message(attribute, value)
        return True
        
    def default_message(self, attribute: str, value: Any) -> str:
        return f"The {attribute} may not be greater than {self.max_length} characters"

class Regex(Rule):
    def __init__(self, pattern: Union[str, Pattern], message: str = None):
        super().__init__(message)
        self.pattern = pattern if isinstance(pattern, Pattern) else re.compile(pattern)
        
    def validate(self, attribute: str, value: Any) -> Union[bool, str]:
        if not value:
            return True
        if not self.pattern.match(str(value)):
            return self.message(attribute, value)
        return True

class In(Rule):
    def __init__(self, values: List[Any], message: str = None):
        super().__init__(message)
        self.values = values
        
    def validate(self, attribute: str, value: Any) -> Union[bool, str]:
        if not value:
            return True
        if value not in self.values:
            return self.message(attribute, value)
        return True
        
    def default_message(self, attribute: str, value: Any) -> str:
        values = ', '.join(str(v) for v in self.values)
        return f"The {attribute} must be one of: {values}"

class Date(Rule):
    def validate(self, attribute: str, value: Any) -> Union[bool, str]:
        if not value:
            return True
        try:
            if isinstance(value, str):
                datetime.fromisoformat(value)
            elif not isinstance(value, datetime):
                return self.message(attribute, value)
            return True
        except ValueError:
            return self.message(attribute, value)
            
    def default_message(self, attribute: str, value: Any) -> str:
        return f"The {attribute} must be a valid date"

class Positive(Rule):
    """Valide que la valeur est un nombre positif"""
    
    def validate(self, attribute: str, value: Any) -> Union[bool, str]:
        if not value:
            return True
        try:
            num = float(value)
            if num <= 0:
                return self.message(attribute, value)
            return True
        except (ValueError, TypeError):
            return self.message(attribute, value)
            
    def default_message(self, attribute: str, value: Any) -> str:
        return f"The {attribute} must be a positive number"

class Link(Rule):
    """Valide que la valeur est une URL valide"""
    
    def validate(self, attribute: str, value: Any) -> Union[bool, str]:
        if not value:
            return True
        pattern = r'^https?:\/\/([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$'
        if not re.match(pattern, str(value)):
            return self.message(attribute, value)
        return True
        
    def default_message(self, attribute: str, value: Any) -> str:
        return f"The {attribute} must be a valid URL"

class Numeric(Rule):
    """Valide que la valeur est un nombre"""
    
    def validate(self, attribute: str, value: Any) -> Union[bool, str]:
        if not value:
            return True
        try:
            float(value)
            return True
        except (ValueError, TypeError):
            return self.message(attribute, value)
            
    def default_message(self, attribute: str, value: Any) -> str:
        return f"The {attribute} must be a number"

class Between(Rule):
    """Valide que la valeur est entre min et max"""
    
    def __init__(self, min_value: float, max_value: float, message: str = None):
        super().__init__(message)
        self.min_value = min_value
        self.max_value = max_value
        
    def validate(self, attribute: str, value: Any) -> Union[bool, str]:
        if not value:
            return True
        try:
            num = float(value)
            if num < self.min_value or num > self.max_value:
                return self.message(attribute, value)
            return True
        except (ValueError, TypeError):
            return self.message(attribute, value)
            
    def default_message(self, attribute: str, value: Any) -> str:
        return f"The {attribute} must be between {self.min_value} and {self.max_value}"

class Boolean(Rule):
    """Valide que la valeur est un booléen"""
    
    def validate(self, attribute: str, value: Any) -> Union[bool, str]:
        if not value:
            return True
        if not isinstance(value, bool) and str(value).lower() not in ('true', 'false', '1', '0'):
            return self.message(attribute, value)
        return True
        
    def default_message(self, attribute: str, value: Any) -> str:
        return f"The {attribute} must be a boolean"

class UUID4(Rule):
    """Valide que la valeur est un UUID v4 valide"""
    
    def validate(self, attribute: str, value: Any) -> Union[bool, str]:
        if not value:
            return True
        pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$'
        if not re.match(pattern, str(value).lower()):
            return self.message(attribute, value)
        return True
        
    def default_message(self, attribute: str, value: Any) -> str:
        return f"The {attribute} must be a valid UUID v4"

class IPAddress(Rule):
    """Valide que la valeur est une adresse IP valide"""
    
    def validate(self, attribute: str, value: Any) -> Union[bool, str]:
        if not value:
            return True
        pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        if not re.match(pattern, str(value)):
            return self.message(attribute, value)
        # Vérifie que chaque octet est entre 0 et 255
        try:
            return all(0 <= int(x) <= 255 for x in str(value).split('.'))
        except (ValueError, TypeError):
            return self.message(attribute, value)
            
    def default_message(self, attribute: str, value: Any) -> str:
        return f"The {attribute} must be a valid IP address" 