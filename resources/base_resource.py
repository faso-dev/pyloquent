from typing import Any, Dict, TypeVar
from libs.pyloquent.model.model import Model

T = TypeVar('T', bound=Model)

class BaseResource:
    """Base class for Resource and ResourceCollection"""
    
    def __init__(self, model: T):
        self.model = model
        
    def to_dict(self) -> Dict[str, Any]:
        """Method to implement in child classes"""
        raise NotImplementedError() 