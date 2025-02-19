from typing import Any, Dict, List, Optional, Union, Callable, Type
from ..interfaces import ResourceInterface

class ConditionalFieldsMixin:
    """Mixin for conditional fields"""
    
    def when(
        self,
        condition: Union[bool, Callable],
        value: Any,
        default: Any = None
    ) -> Optional[Any]:
        """
        Include a field conditionally.
        
        Example:
            'is_admin': self.when(user.is_admin, True)
        """
        if callable(condition):
            condition = condition(self.model)
        # If the condition is false and default is None, return None
        # which will cause the field to be omitted from the JSON
        return value if condition else default
        
    def when_loaded(
        self,
        relation: str,
        callback: Optional[Callable] = None,
        default: Any = None
    ) -> Optional[Any]:
        """
        Include a relation only if it has been explicitly loaded.
        
        Example:
            'author': self.when_loaded('author', lambda author: {
                'id': author.id,
                'name': author.name
            })
        """
        # Check if the relation has been explicitly loaded
        if not hasattr(self.model, '_loaded_relations') or relation not in self.model._loaded_relations:
            # Return None to omit the field from the JSON
            return None
            
        # Get the relation
        value = getattr(self.model, relation)
        
        # Apply the callback if provided
        return callback(value) if callback and value else value

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the resource to a dictionary, omitting None values.
        """
        data = super().to_dict()
        print(data)
        # Filter out None values
        return {k: v for k, v in data.items() if v is not None}

class RelationshipFieldsMixin:
    """Mixin for relationship fields"""
    
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