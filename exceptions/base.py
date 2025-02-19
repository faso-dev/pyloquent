class PyloquentException(Exception):
    """Exception de base pour toutes les erreurs Pyloquent"""
    pass

class ValidationException(PyloquentException):
    """Exception de base pour les erreurs de validation"""
    pass

class DatabaseException(PyloquentException):
    """Exception de base pour les erreurs de base de données"""
    pass

class RelationException(PyloquentException):
    """Exception de base pour les erreurs de relations"""
    pass

class ModelException(PyloquentException):
    """Exception de base pour les erreurs de modèle"""
    pass 