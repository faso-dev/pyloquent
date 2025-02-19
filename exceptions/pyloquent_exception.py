from typing import Any, Dict, List, Optional

class PyloquentException(Exception):
    """
    Exception de base pour toutes les erreurs de Pyloquent.
    
    Example:
        try:
            user.save()
        except PyloquentException as e:
            print(f"Une erreur est survenue: {e}")
    """
    def __init__(self, message: str, code: Optional[str] = None):
        self.message = message
        self.code = code
        super().__init__(message)

class ValidationException(PyloquentException):
    """
    Exception levée lors d'erreurs de validation.
    
    Example:
        try:
            user.save()
        except ValidationException as e:
            print("Erreurs de validation:")
            for field, errors in e.errors.items():
                print(f"{field}: {', '.join(errors)}")
    """
    def __init__(self, errors: Dict[str, List[str]]):
        self.errors = errors
        super().__init__("Validation failed", "VALIDATION_ERROR")

class RelationNotLoadedException(PyloquentException):
    """
    Exception levée lors de l'accès à une relation non chargée.
    
    Example:
        try:
            user.posts  # Si posts n'est pas chargé
        except RelationNotLoadedException as e:
            posts = user.load('posts')  # Charge la relation
    """
    def __init__(self, relation: str, model: str):
        super().__init__(
            f"La relation '{relation}' n'est pas chargée sur le modèle {model}. "
            f"Utilisez with_('{relation}') ou load('{relation}') pour la charger.",
            "RELATION_NOT_LOADED"
        )

class InvalidQueryException(PyloquentException):
    """
    Exception levée lors de la construction de requêtes invalides.
    
    Example:
        try:
            User.where('invalid_field', '=', 'value').get()
        except InvalidQueryException as e:
            print(f"Erreur de requête: {e}")
    """
    def __init__(self, message: str):
        super().__init__(message, "INVALID_QUERY") 
        
class ModelNotFoundException(PyloquentException):
    """
    Exception levée lorsqu'un modèle n'est pas trouvé.
    
    Example:
        try:
            user = User.find_or_fail(100)
        except ModelNotFoundException as e:
            print(f"Modèle non trouvé: {e}")
    """
    def __init__(self, model: str, id: Any):
        super().__init__(f"Modèle {model} non trouvé pour l'ID {id}", "MODEL_NOT_FOUND")
