from datetime import datetime
from typing import Any, Optional
from .interfaces import CastInterface

class DateTimeCast(CastInterface[datetime]):
    """
    Cast pour les champs datetime.
    
    Example:
        class User(Model):
            _casts = {
                'created_at': 'datetime'
            }
            
        user.created_at = '2023-01-01 12:00:00'
        # Stocké comme datetime en base
        # Accessible comme user.created_at.strftime()
    """
    
    def to_python(self, value: Any) -> Optional[datetime]:
        if value is None:
            return None
        if isinstance(value, datetime):
            return value
        try:
            return datetime.fromisoformat(str(value))
        except (ValueError, TypeError):
            return None
            
    def to_database(self, value: Optional[datetime]) -> Optional[str]:
        if value is None:
            return None
        if isinstance(value, datetime):
            return value.isoformat()
        try:
            return datetime.fromisoformat(str(value)).isoformat()
        except (ValueError, TypeError):
            return None 