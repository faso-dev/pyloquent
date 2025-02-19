from typing import Callable, Dict, List, Any
from .interfaces import EventDispatcherInterface

class EventDispatcher(EventDispatcherInterface):
    """Gestionnaire d'événements centralisé"""
    
    _listeners: Dict[str, List[Callable]] = {}
    _wildcards: List[Callable] = []
    
    @classmethod
    def listen(cls, event: str, callback: Callable) -> None:
        """Ajoute un listener pour un événement spécifique"""
        if event not in cls._listeners:
            cls._listeners[event] = []
        cls._listeners[event].append(callback)
        
    @classmethod
    def listen_any(cls, callback: Callable) -> None:
        """Ajoute un listener pour tous les événements"""
        cls._wildcards.append(callback)
        
    @classmethod
    def dispatch(cls, event: str, model: Any, *args) -> None:
        """Dispatch un événement aux listeners"""
        # Appelle les wildcards
        for listener in cls._wildcards:
            listener(event, model, *args)
            
        # Appelle les listeners spécifiques
        if event in cls._listeners:
            for listener in cls._listeners[event]:
                listener(model, *args) 