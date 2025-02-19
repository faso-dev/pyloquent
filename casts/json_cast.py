import json
from typing import Any, Dict
from .interfaces import CastInterface

class JsonCast(CastInterface[Dict]):
    """
    Cast pour les champs JSON/dictionnaire.
    
    Example:
        class User(Model):
            _casts = {
                'settings': 'json'
            }
            
        user = User(settings={'theme': 'dark'})
        # Stocké comme '{"theme": "dark"}' en base
        # Accessible comme user.settings['theme']
    """
    
    def to_python(self, value: Any) -> Dict:
        if value is None:
            return {}
        if isinstance(value, dict):
            return value
        try:
            return json.loads(value)
        except (TypeError, json.JSONDecodeError):
            return {}
            
    def to_database(self, value: Dict) -> str:
        if value is None:
            return None
        if isinstance(value, str):
            try:
                # Vérifie que c'est du JSON valide
                json.loads(value)
                return value
            except json.JSONDecodeError:
                return json.dumps({})
        return json.dumps(value) 