from .base import ModelException

class ModelNotFoundException(ModelException):
    """Levée quand un modèle n'est pas trouvé"""
    pass

class AttributeException(ModelException):
    """Levée pour les erreurs d'attributs"""
    pass

class InvalidQueryException(ModelException):
    """Levée quand une requête est invalide"""
    pass

class MassAssignmentException(ModelException):
    """Levée quand l'assignation en masse échoue"""
    pass 