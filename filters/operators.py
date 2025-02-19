from enum import Enum
from typing import Any

class Operator(Enum):
    """
    Opérateurs de comparaison supportés pour les filtres.
    
    Example:
        # Comparaisons basiques
        User.where('age', Operator.GREATER_THAN, 18)
        
        # Recherche insensible à la casse
        User.where('name', Operator.ILIKE, '%john%')
        
        # Recherche dans une liste
        User.where('status', Operator.IN, ['active', 'pending'])
        
        # Vérification de nullité
        User.where('deleted_at', Operator.NULL)
    """
    EQUAL = '='
    NOT_EQUAL = '!='
    GREATER_THAN = '>'
    GREATER_THAN_OR_EQUAL = '>='
    LESS_THAN = '<'
    LESS_THAN_OR_EQUAL = '<='
    LIKE = 'LIKE'
    ILIKE = 'ILIKE'
    IN = 'IN'
    NOT_IN = 'NOT IN'
    NULL = 'IS NULL'
    NOT_NULL = 'IS NOT NULL'
    BETWEEN = 'BETWEEN'
    NOT_BETWEEN = 'NOT BETWEEN'
    
    @classmethod
    def validate(cls, operator: str) -> bool:
        """
        Vérifie si l'opérateur est valide.
        
        Args:
            operator: Opérateur à valider
            
        Returns:
            bool: True si l'opérateur est valide
            
        Example:
            Operator.validate('=')  # True
            Operator.validate('INVALID')  # False
        """
        return any(op.value == operator for op in cls)
        
    @classmethod
    def requires_value(cls, operator: str) -> bool:
        """
        Vérifie si l'opérateur nécessite une valeur.
        
        Args:
            operator: Opérateur à vérifier
            
        Returns:
            bool: True si l'opérateur nécessite une valeur
            
        Example:
            Operator.requires_value('=')  # True
            Operator.requires_value('IS NULL')  # False
        """
        return operator not in (cls.NULL.value, cls.NOT_NULL.value)
        
    @classmethod
    def requires_array(cls, operator: str) -> bool:
        """
        Vérifie si l'opérateur nécessite un tableau de valeurs.
        
        Args:
            operator: Opérateur à vérifier
            
        Returns:
            bool: True si l'opérateur nécessite un tableau
            
        Example:
            Operator.requires_array('IN')  # True
            Operator.requires_array('=')  # False
        """
        return operator in (cls.IN.value, cls.NOT_IN.value, 
                          cls.BETWEEN.value, cls.NOT_BETWEEN.value)
                          
    @classmethod
    def is_pattern_match(cls, operator: str) -> bool:
        """
        Vérifie si l'opérateur est un opérateur de pattern matching.
        
        Args:
            operator: Opérateur à vérifier
            
        Returns:
            bool: True si l'opérateur est un pattern matching
            
        Example:
            Operator.is_pattern_match('LIKE')  # True
            Operator.is_pattern_match('ILIKE')  # True
            Operator.is_pattern_match('=')  # False
        """
        return operator in (cls.LIKE.value, cls.ILIKE.value) 