from typing import Any, Dict, Optional
import sqlalchemy as sa
from .interfaces import ColumnType

class Column:
    """
    Helper pour la création de colonnes.
    
    Example:
        Column.string('name', 100).nullable()
        Column.integer('age').unsigned()
        Column.enum('status', ['active', 'inactive']).default('active')
    """
    
    @classmethod
    def integer(cls, name: str) -> sa.Column:
        return sa.Column(name, sa.Integer())
        
    @classmethod
    def string(cls, name: str, length: int = 255) -> sa.Column:
        return sa.Column(name, sa.String(length))
        
    @classmethod
    def text(cls, name: str) -> sa.Column:
        return sa.Column(name, sa.Text())
        
    @classmethod
    def datetime(cls, name: str) -> sa.Column:
        return sa.Column(name, sa.DateTime())
        
    @classmethod
    def boolean(cls, name: str) -> sa.Column:
        return sa.Column(name, sa.Boolean())
        
    @classmethod
    def decimal(cls, name: str, precision: int = 8, scale: int = 2) -> sa.Column:
        return sa.Column(name, sa.Numeric(precision, scale))
        
    @classmethod
    def json(cls, name: str) -> sa.Column:
        return sa.Column(name, sa.JSON())
        
    @classmethod
    def uuid(cls, name: str) -> sa.Column:
        return sa.Column(name, sa.UUID()) 