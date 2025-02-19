from typing import Any, Dict, List, Optional, Union, Callable, Type
from ..interfaces import ResourceInterface

class ConditionalFieldsMixin:
    """Mixin pour les champs conditionnels"""
    
    def when(
        self,
        condition: Union[bool, Callable],
        value: Any,
        default: Any = None
    ) -> Any:
        if callable(condition):
            condition = condition(self.model)
        return value if condition else default
        
    def when_loaded(
        self,
        relation: str,
        callback: Optional[Callable] = None,
        default: Any = None
    ) -> Any:
        """
        Inclut une relation seulement si elle a été explicitement chargée.
        
        Example:
            # Ne sera inclus que si author a été chargé avec with_()
            'author': self.when_loaded('author', lambda author: {
                'id': author.id,
                'name': author.name
            })
        """
        # Vérifie si la relation a été explicitement chargée
        if not hasattr(self.model, '_loaded_relations') or relation not in self.model._loaded_relations:
            return default
            
        # Récupère la relation
        value = getattr(self.model, relation)
        
        # Applique le callback si fourni
        return callback(value) if callback and value else value

class RelationshipFieldsMixin:
    """Mixin pour les champs de relation"""
    
    def relation(
        self,
        name: str,
        resource: Type[ResourceInterface],
        transformer: Optional[Callable] = None
    ) -> Any:
        if not hasattr(self.model, name):
            return None
        related = getattr(self.model, name)
        if transformer and related:
            related = transformer(related)
        return resource(related).to_dict() if related else None 