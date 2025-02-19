from typing import Any, Callable, Optional, TypeVar, Type, Union
from libs.pyloquent.model.model import Model

T = TypeVar('T', bound=Model)

class ConditionalFields:
    """
    Mixin pour gérer les champs conditionnels dans les Resources.
    
    Example:
        class UserResource(Resource):
            def to_dict(self):
                return {
                    'id': self.model.id,
                    'email': self.when(
                        self.model.is_public,
                        self.model.email
                    ),
                    
                    # Inclusion conditionnelle de relation
                    'posts': self.when_loaded('posts',
                        PostResource.collection
                    ),
                    
                    # Transformation conditionnelle
                    'status': self.when(
                        self.model.is_premium,
                        lambda m: 'premium',
                        'basic'
                    ),
                    
                    # Fusion conditionnelle
                    **self.merge_when(self.model.is_admin, {
                        'permissions': self.model.permissions,
                        'last_login': str(self.model.last_login)
                    })
                }
    """
    
    def when(
        self,
        condition: bool,
        value: Any,
        default: Any = None
    ) -> Any:
        """
        Inclut une valeur conditionnellement.
        
        Args:
            condition: Condition à évaluer
            value: Valeur à inclure si vrai
            default: Valeur par défaut si faux
        """
        if callable(condition):
            condition = condition(self.model)
            
        if callable(value):
            value = value(self.model)
            
        return value if condition else default
        
    def when_loaded(
        self,
        relation: str,
        callback: Optional[Union[Callable, Type['Resource']]] = None,
        default: Any = None
    ) -> Any:
        """
        Inclut une relation seulement si elle est chargée.
        
        Args:
            relation: Nom de la relation
            callback: Fonction de transformation ou Resource
            default: Valeur par défaut si non chargée
        """
        if not hasattr(self.model, relation):
            return default
            
        value = getattr(self.model, relation)
        
        if callback is None:
            return value
            
        if isinstance(callback, type) and issubclass(callback, Resource):
            return callback.collection(value)
            
        return callback(value)
        
    def merge_when(
        self,
        condition: bool,
        attributes: dict
    ) -> dict:
        """
        Fusionne un dictionnaire conditionnellement.
        
        Args:
            condition: Condition à évaluer
            attributes: Attributs à fusionner si vrai
        """
        if callable(condition):
            condition = condition(self.model)
            
        return attributes if condition else {} 