from typing import Any, Dict, List, Optional, Callable, Union, TypeVar, Iterator
from functools import reduce
from .interfaces import CollectionInterface

T = TypeVar('T')

class Collection(CollectionInterface[T], list):
    """
    Collection améliorée avec des méthodes inspirées de Laravel.
    
    Example:
        users = Collection([
            User(name='John', age=25),
            User(name='Jane', age=30)
        ])
        
        # Filtrage
        adults = users.where('age', '>=', 18)
        
        # Agrégation
        average_age = users.avg('age')
        
        # Transformation
        names = users.pluck('name')
        
        # Groupement
        by_age = users.group_by('age')
        
        # Réduction
        total = users.sum('amount')
        
        # Recherche
        admin = users.first_where('role', 'admin')
    """
    
    def __init__(self, items: Optional[List[T]] = None):
        super().__init__(items or [])
        
    def all(self) -> List[T]:
        """Retourne tous les éléments"""
        return list(self)
        
    def avg(self, key: Optional[str] = None) -> float:
        """
        Calcule la moyenne d'une colonne.
        
        Example:
            avg_age = users.avg('age')
            avg_score = scores.avg()  # Si les éléments sont des nombres
        """
        if not self:
            return 0.0
            
        if key is None:
            return sum(float(item) for item in self) / len(self)
            
        return sum(float(self._get_value(item, key)) for item in self) / len(self)
        
    def chunk(self, size: int) -> 'Collection[Collection[T]]':
        """
        Divise la collection en morceaux.
        
        Example:
            for chunk in users.chunk(100):
                process_users(chunk)
        """
        return Collection(
            Collection(self[i:i + size])
            for i in range(0, len(self), size)
        )
        
    def contains(self, key: Union[str, Callable[[T], bool]], value: Any = None) -> bool:
        """
        Vérifie si un élément existe.
        
        Example:
            # Avec callback
            has_admin = users.contains(lambda u: u.role == 'admin')
            
            # Avec clé/valeur
            has_john = users.contains('name', 'John')
        """
        if callable(key):
            return any(key(item) for item in self)
            
        return any(self._get_value(item, key) == value for item in self)
        
    def count(self) -> int:
        """Compte les éléments"""
        return len(self)
        
    def each(self, callback: Callable[[T], None]) -> 'Collection[T]':
        """
        Itère sur chaque élément.
        
        Example:
            users.each(lambda user: user.notify())
        """
        for item in self:
            callback(item)
        return self
        
    def filter(self, callback: Callable[[T], bool]) -> 'Collection[T]':
        """
        Filtre les éléments.
        
        Example:
            adults = users.filter(lambda u: u.age >= 18)
        """
        return Collection(item for item in self if callback(item))
        
    def first(self, callback: Optional[Callable[[T], bool]] = None) -> Optional[T]:
        """
        Retourne le premier élément.
        
        Example:
            first_user = users.first()
            first_admin = users.first(lambda u: u.role == 'admin')
        """
        if callback is None:
            return self[0] if self else None
            
        return next((item for item in self if callback(item)), None)
        
    def group_by(self, key: Union[str, Callable[[T], Any]]) -> Dict[Any, 'Collection[T]']:
        """
        Groupe les éléments.
        
        Example:
            by_role = users.group_by('role')
            by_age_group = users.group_by(lambda u: u.age // 10 * 10)
        """
        groups: Dict[Any, Collection[T]] = {}
        
        for item in self:
            group_key = key(item) if callable(key) else self._get_value(item, key)
            
            if group_key not in groups:
                groups[group_key] = Collection()
                
            groups[group_key].append(item)
            
        return groups
        
    def map(self, callback: Callable[[T], Any]) -> 'Collection':
        """
        Transforme les éléments.
        
        Example:
            names = users.map(lambda u: u.name)
        """
        return Collection(callback(item) for item in self)
        
    def pluck(self, key: str, value_key: Optional[str] = None) -> Union['Collection', Dict]:
        """
        Extrait une colonne.
        
        Example:
            names = users.pluck('name')
            id_name_map = users.pluck('name', 'id')  # {1: 'John', 2: 'Jane'}
        """
        if value_key is None:
            return Collection(self._get_value(item, key) for item in self)
            
        return {
            self._get_value(item, value_key): self._get_value(item, key)
            for item in self
        }
        
    def where(self, key: str, operator: str, value: Any) -> 'Collection[T]':
        """
        Filtre par une condition.
        
        Example:
            adults = users.where('age', '>=', 18)
            active = users.where('status', '=', 'active')
        """
        ops = {
            '=': lambda a, b: a == b,
            '!=': lambda a, b: a != b,
            '>': lambda a, b: a > b,
            '>=': lambda a, b: a >= b,
            '<': lambda a, b: a < b,
            '<=': lambda a, b: a <= b,
            'in': lambda a, b: a in b,
            'not in': lambda a, b: a not in b,
        }
        
        if operator not in ops:
            raise ValueError(f"Opérateur non supporté: {operator}")
            
        return Collection(
            item for item in self
            if ops[operator](self._get_value(item, key), value)
        )
        
    def _get_value(self, item: T, key: str) -> Any:
        """Récupère une valeur par sa clé"""
        if hasattr(item, key):
            return getattr(item, key)
        if hasattr(item, '__getitem__'):
            return item[key]
        raise ValueError(f"Impossible d'accéder à la clé {key}") 
    
def collect(items: List[T]) -> Collection[T]:
    return Collection(items)

