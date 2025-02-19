from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
from enum import Enum

class ColumnType(Enum):
    """Types de colonnes supportés"""
    INTEGER = "integer"
    STRING = "string"
    TEXT = "text"
    BOOLEAN = "boolean"
    DATETIME = "datetime"
    DATE = "date"
    DECIMAL = "decimal"
    FLOAT = "float"
    JSON = "json"
    UUID = "uuid"

class TableOperation(Enum):
    """Types d'opérations sur les tables"""
    CREATE = "create"
    ALTER = "alter"
    DROP = "drop"
    RENAME = "rename"

class MigrationInterface(ABC):
    """Interface pour les migrations"""
    
    @abstractmethod
    def create_table(self, name: str, **options) -> None:
        pass
        
    @abstractmethod
    def alter_table(self, name: str, **options) -> None:
        pass
        
    @abstractmethod
    def drop_table(self, name: str) -> None:
        pass
        
    @abstractmethod
    def rename_table(self, old: str, new: str) -> None:
        pass 