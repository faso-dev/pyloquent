from typing import Any, Dict, List, Optional, Type, TypeVar, Callable
from faker import Faker
import random

from .interfaces import FactoryInterface
from ..types import ModelType

T = TypeVar('T', bound=ModelType)

class Factory(FactoryInterface[T]):
    """
    Classe de base pour créer des factories de modèles.
    
    Example:
        class UserFactory(Factory[User]):
            model = User
            
            def definition(self):
                return {
                    'name': self.faker.name(),
                    'email': self.faker.email(),
                    'password': self.faker.password(),
                    'is_active': True
                }
                
        # Utilisation
        user = UserFactory().create()
        users = UserFactory().create_many(5)
        
        # Avec attributs personnalisés
        admin = UserFactory().create(
            role='admin',
            is_active=True
        )
    """
    
    model: Type[T]
    
    def __init__(self):
        self.faker = Faker()
        
    def definition(self) -> Dict[str, Any]:
        """À surcharger dans les classes enfants"""
        raise NotImplementedError()
        
    def make(self, **attributes) -> T:
        """Crée une instance sans sauvegarder"""
        data = {**self.definition(), **attributes}
        return self.model(**data)
        
    def create(self, **attributes) -> T:
        """Crée et sauvegarde une instance"""
        instance = self.make(**attributes)
        instance.save()
        return instance
        
    def make_many(self, count: int, **attributes) -> List[T]:
        """Crée plusieurs instances sans sauvegarder"""
        return [self.make(**attributes) for _ in range(count)]
        
    def create_many(self, count: int, **attributes) -> List[T]:
        """Crée et sauvegarde plusieurs instances"""
        return [self.create(**attributes) for _ in range(count)]
        
    def state(self, **attributes) -> 'Factory[T]':
        """Définit des attributs par défaut"""
        self._state = attributes
        return self
        
    def sequence(self, callback: Callable[[int], Any]) -> Any:
        """Génère des valeurs séquentielles"""
        if not hasattr(self, '_sequence'):
            self._sequence = 0
        self._sequence += 1
        return callback(self._sequence) 