from typing import ClassVar, Dict, List, Callable, Any, Optional, Type
from .dispatcher import EventDispatcher
from .observer import Observer

class Observable:
    """
    Classe de base pour les objets qui peuvent émettre des événements.
    
    Example:
        class User(Model, Observable):
            def on_creating(self):
                self.password = hash_password(self.password)
                
            def on_created(self):
                send_welcome_email(self)
    """
    
    # Événements par défaut
    _events: ClassVar[List[str]] = [
        'creating', 'created',
        'updating', 'updated',
        'deleting', 'deleted',
        'saving', 'saved',
        'restoring', 'restored'
    ]
    
    # Observers de la classe
    _observers: ClassVar[List[Type[Observer]]] = []
    
    @classmethod
    def observe(cls, observer: Type[Observer]) -> None:
        """Ajoute un observer à la classe"""
        cls._observers.append(observer)
        observer.register(cls)
        
    def fire_event(self, event: str, *args) -> None:
        """
        Déclenche un événement.
        
        Args:
            event: Nom de l'événement
            *args: Arguments supplémentaires
        """
        # Appelle d'abord la méthode spécifique si elle existe
        method = f'on_{event}'
        if hasattr(self, method):
            getattr(self, method)(*args)
            
        # Déclenche l'événement global
        EventDispatcher.dispatch(
            f"{self.__class__.__name__}.{event}",
            self,
            *args
        ) 