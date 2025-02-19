from typing import Any, Dict, TypeVar
from libs.pyloquent.model.model import Model

T = TypeVar('T', bound=Model)

class BaseResource:
    """Classe de base pour Resource et ResourceCollection"""
    
    def __init__(self, model: T):
        self.model = model
        
    def to_dict(self) -> Dict[str, Any]:
        """Méthode à implémenter par les classes enfants"""
        raise NotImplementedError() 