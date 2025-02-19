from .base import RelationException

class RelationNotLoadedException(RelationException):
    """Levée quand on accède à une relation non chargée"""
    
    def __init__(self, relation: str, model: str):
        self.relation = relation
        self.model = model
        super().__init__(
            f"La relation '{relation}' n'est pas chargée sur le modèle {model}"
        )

class InvalidRelationException(RelationException):
    """Levée quand une relation est invalide"""
    pass

class MorphRelationException(RelationException):
    """Levée pour les erreurs de relations polymorphiques"""
    pass 