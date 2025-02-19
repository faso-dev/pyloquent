from typing import Any, Dict, List, Type, Optional, ClassVar, TypeVar
from pydantic import BaseModel

from .interfaces import ResourceInterface
from .concerns.mixins import ConditionalFieldsMixin, RelationshipFieldsMixin
from ..types import ModelType

T = TypeVar('T', bound=ModelType)

class Resource(ResourceInterface[T], ConditionalFieldsMixin, RelationshipFieldsMixin):
    """Resource de base pour la transformation de modèles"""
    
    Schema: ClassVar[Optional[Type[BaseModel]]] = None
    
    def __init__(self, model: T) -> None:
        self.model = model
        self._additional: Dict[str, Any] = {}
        
    def to_dict(self) -> Dict[str, Any]:
        if self.Schema:
            return self.Schema.model_validate(self.model).model_dump()
        return self._to_dict()
        
    def _to_dict(self) -> Dict[str, Any]:
        """À implémenter dans les classes enfants"""
        raise NotImplementedError()
        
    @classmethod
    def collection(cls, models: List[T]) -> 'ResourceCollection':
        from .resource_collection import ResourceCollection
        return ResourceCollection([cls(model) for model in models]) 