from typing import Type, Any
from .interfaces import ObserverInterface
from .dispatcher import EventDispatcher

class Observer(ObserverInterface):
    """Base class pour les observers de modèles"""
    
    @classmethod
    def register(cls, model_class: Type[Any]) -> None:
        """Enregistre les méthodes de l'observer comme listeners"""
        for event in getattr(model_class, '_events', []):
            if hasattr(cls, event):
                EventDispatcher.listen(
                    f"{model_class.__name__}.{event}",
                    getattr(cls, event)
                ) 