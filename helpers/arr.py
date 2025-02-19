from typing import Any, List, Dict, Callable, Optional, Union, TypeVar
from copy import deepcopy

T = TypeVar('T')

class Arr:
    """
    Helper pour la manipulation des tableaux.
    
    Example:
        # Accès aux données
        Arr.get(['a', 'b'], 0)  # 'a'
        Arr.first(['a', 'b'])  # 'a'
        
        # Manipulation
        Arr.except(['a', 'b', 'c'], ['a'])  # ['b', 'c']
        Arr.only(['a', 'b', 'c'], ['a', 'b'])  # ['a', 'b']
    """
    
    @staticmethod
    def get(array: List[T], key: int, default: Any = None) -> T:
        """
        Récupère un élément d'un tableau par son index.
        
        Example:
            Arr.get(['a', 'b'], 0)  # 'a'
            Arr.get(['a', 'b'], 2, 'default')  # 'default'
        """
        try:
            return array[key]
        except (IndexError, KeyError):
            return default
            
    @staticmethod
    def first(array: List[T], default: Any = None) -> T:
        """
        Récupère le premier élément d'un tableau.
        
        Example:
            Arr.first(['a', 'b'])  # 'a'
            Arr.first([], 'default')  # 'default'
        """
        return Arr.get(array, 0, default)
        
    @staticmethod
    def last(array: List[T], default: Any = None) -> T:
        """
        Récupère le dernier élément d'un tableau.
        
        Example:
            Arr.last(['a', 'b'])  # 'b'
            Arr.last([], 'default')  # 'default'
        """
        return Arr.get(array, -1, default)
        
    @staticmethod
    def except_(array: List[T], keys: List[Any]) -> List[T]:
        """
        Retourne un tableau sans les éléments spécifiés.
        
        Example:
            Arr.except(['a', 'b', 'c'], ['a'])  # ['b', 'c']
            Arr.except([1, 2, 3, 4], [1, 3])  # [2, 4]
        """
        return [item for item in array if item not in keys]
        
    @staticmethod
    def only(array: List[T], keys: List[Any]) -> List[T]:
        """
        Retourne un tableau avec uniquement les éléments spécifiés.
        
        Example:
            Arr.only(['a', 'b', 'c'], ['a', 'b'])  # ['a', 'b']
            Arr.only([1, 2, 3, 4], [2, 4])  # [2, 4]
        """
        return [item for item in array if item in keys]
        
    @staticmethod
    def pluck(array: List[Dict], key: str, value_key: Optional[str] = None) -> Union[List, Dict]:
        """
        Extrait une liste de valeurs d'un tableau de dictionnaires.
        
        Example:
            items = [{'id': 1, 'name': 'a'}, {'id': 2, 'name': 'b'}]
            Arr.pluck(items, 'name')  # ['a', 'b']
            Arr.pluck(items, 'name', 'id')  # {1: 'a', 2: 'b'}
        """
        if value_key is None:
            return [item[key] for item in array if key in item]
        return {item[value_key]: item[key] for item in array if key in item and value_key in item}
        
    @staticmethod
    def where(array: List[Dict], key: str, operator: str = '=', value: Any = None) -> List[Dict]:
        """
        Filtre un tableau de dictionnaires.
        
        Example:
            items = [{'id': 1, 'active': True}, {'id': 2, 'active': False}]
            Arr.where(items, 'active', '=', True)  # [{'id': 1, 'active': True}]
        """
        if value is None:
            value = operator
            operator = '='
            
        def compare(item_value: Any, op: str, compare_value: Any) -> bool:
            if op == '=':
                return item_value == compare_value
            elif op == '!=':
                return item_value != compare_value
            elif op == '>':
                return item_value > compare_value
            elif op == '>=':
                return item_value >= compare_value
            elif op == '<':
                return item_value < compare_value
            elif op == '<=':
                return item_value <= compare_value
            elif op == 'in':
                return item_value in compare_value
            elif op == 'not in':
                return item_value not in compare_value
            return False
            
        return [
            item for item in array 
            if key in item and compare(item[key], operator, value)
        ]
        
    @staticmethod
    def map(array: List[T], callback: Callable[[T], Any]) -> List[Any]:
        """
        Applique une fonction à chaque élément du tableau.
        
        Example:
            Arr.map([1, 2, 3], lambda x: x * 2)  # [2, 4, 6]
        """
        return [callback(item) for item in array]
        
    @staticmethod
    def filter(array: List[T], callback: Callable[[T], bool]) -> List[T]:
        """
        Filtre un tableau selon une fonction.
        
        Example:
            Arr.filter([1, 2, 3, 4], lambda x: x % 2 == 0)  # [2, 4]
        """
        return [item for item in array if callback(item)]
        
    @staticmethod
    def reduce(array: List[T], callback: Callable[[Any, T], Any], initial: Any = None) -> Any:
        """
        Réduit un tableau à une seule valeur.
        
        Example:
            Arr.reduce([1, 2, 3], lambda acc, x: acc + x)  # 6
            Arr.reduce([1, 2, 3], lambda acc, x: acc + x, 10)  # 16
        """
        result = initial
        for item in array:
            if result is None:
                result = item
            else:
                result = callback(result, item)
        return result
        
    @staticmethod
    def unique(array: List[T]) -> List[T]:
        """
        Retourne un tableau sans doublons.
        
        Example:
            Arr.unique([1, 2, 2, 3, 3, 3])  # [1, 2, 3]
        """
        return list(dict.fromkeys(array))
        
    @staticmethod
    def chunk(array: List[T], size: int) -> List[List[T]]:
        """
        Divise un tableau en morceaux de taille donnée.
        
        Example:
            Arr.chunk([1, 2, 3, 4, 5], 2)  # [[1, 2], [3, 4], [5]]
        """
        return [array[i:i + size] for i in range(0, len(array), size)]
