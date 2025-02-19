from .base import DatabaseException

class ConnectionException(DatabaseException):
    """Levée quand la connexion à la base échoue"""
    pass

class QueryException(DatabaseException):
    """Levée quand une requête est invalide"""
    pass

class TransactionException(DatabaseException):
    """Levée quand une transaction échoue"""
    pass

class MigrationException(DatabaseException):
    """Levée quand une migration échoue"""
    pass

class DeadlockException(DatabaseException):
    """Levée en cas de deadlock"""
    pass 