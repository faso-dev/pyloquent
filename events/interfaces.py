from abc import ABC, abstractmethod
from typing import Any, Callable, List, Type, TypeVar

ModelType = TypeVar('ModelType')

class EventDispatcherInterface(ABC):
    """Interface pour le dispatcher d'événements"""
    
    @abstractmethod
    def listen(self, event: str, callback: Callable) -> None:
        pass
        
    @abstractmethod
    def dispatch(self, event: str, model: Any, *args) -> None:
        pass

class ObserverInterface(ABC):
    """Interface pour les observers"""
    
    @abstractmethod
    def register(self, model_class: Type[Any]) -> None:
        pass 