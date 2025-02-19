from typing import Type, TypeVar, ClassVar, List, Dict, Any, Optional, TYPE_CHECKING
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from datetime import datetime

from ..model.base import Base
from ..builder import QueryBuilder, AggregateBuilder
from ..scopes import GlobalScope
from ..model.attributes import AttributeCaster
from ..events import Observable
from ..validation import Validator, ValidationError, Rule
from pydantic import BaseModel, create_model
from ..casts import CastRegistry
from ..casts.cast import Cast
from ..model.registry import ModelRegistry

if TYPE_CHECKING:
    from ..relations import BelongsTo, HasMany, HasOne

T = TypeVar('T', bound='Model')

class Model(Base, Observable):
    """
    Classe de base pour tous les modèles Pyloquent.
    
    Exemple d'utilisation:
        class User(Model):
            _table_name = 'users'
            _casts = {
                'id': 'uuid',
                'is_active': 'bool',
                'settings': 'json'
            }
            
            def posts(self):
                return self.has_many(Post, 'user_id')
                
        # Création
        user = User.create(name='John', email='john@example.com')
        
        # Requêtes
        active_users = User.query()\
            .where('is_active', True)\
            .with_('posts')\
            .get()
    """
    
    __abstract__ = True
    
    # Class level attributes
    _table_name: ClassVar[str]
    _connection: ClassVar[Any] = None
    _session_factory: ClassVar[Any] = None
    _session: ClassVar[Any] = None
    _primary_key: ClassVar[str] = 'id'
    _timestamps: ClassVar[bool] = True
    _soft_deletes: ClassVar[bool] = False
    
    # Attribute casting
    _casts: ClassVar[Dict[str, str]] = {}
    _dates: ClassVar[List[str]] = ['created_at', 'updated_at']
    
    # Scopes
    _global_scopes: ClassVar[List[Type[GlobalScope]]] = []
    
    _rules: ClassVar[Dict[str, List[Rule]]] = {}
    
    # Pydantic schema optionnel
    Schema: ClassVar[Optional[Type[BaseModel]]] = None
    
    _relations: Dict[str, Any] = {}
    _loaded_relations: ClassVar[set] = set()
    
    def __init__(self, **attributes):
        super().__init__()
        self._attributes = attributes
        self._relations = {}
        self._loaded_relations = set()
    
    def _get_attribute(self, key: str) -> Any:
        """Récupère un attribut avec cast si nécessaire"""
        value = self._attributes.get(key)
        
        if key in self._casts:
            return AttributeCaster.cast(value, self._casts[key])
            
        if key in self._dates and value is not None:
            return datetime.fromisoformat(value) if isinstance(value, str) else value
            
        return value
        
    def _set_attribute(self, key: str, value: Any):
        """Définit un attribut avec cast si nécessaire"""
        if key in self._casts:
            value = AttributeCaster.cast(value, self._casts[key])
            
        self._attributes[key] = value
    
    @classmethod
    def query(cls) -> QueryBuilder:
        """Obtient une nouvelle instance de QueryBuilder"""
        builder = QueryBuilder(cls)
        
        # Applique les scopes globaux
        for scope_class in cls._global_scopes:
            scope = scope_class()
            if scope.should_apply(cls):
                builder = scope.apply(builder)
            
        return builder
    
    @classmethod
    def with_trashed(cls):
        """Inclut les éléments soft-deleted"""
        return cls.query().with_trashed()
    
    def validate(self):
        """Valide le modèle selon les règles définies"""
        validator = Validator(self._attributes, self._rules)
        return validator.validate()
    
    @classmethod
    def create(cls, **attributes) -> T:
        """
        Crée et sauvegarde une nouvelle instance du modèle.
        
        Args:
            **attributes: Attributs du modèle
            
        Returns:
            Une nouvelle instance sauvegardée
            
        Example:
            user = User.create(
                name='John',
                email='john@example.com',
                password='secret'
            )
        """
        instance = cls(**attributes)
        instance.save()
        return instance
        
    def save(self):
        """
        Sauvegarde le modèle avec validation et événements.
        
        Raises:
            ValidationError: Si la validation échoue
        """
        self.fire_event('saving')
        
        if self._rules and not self.validate():
            raise ValidationError(self.validator.errors)
            
        session = self.get_session()
        try:
            is_new = not hasattr(self, 'id') or self.id is None
            
            if is_new:
                self.fire_event('creating')
                
            else:
                self.fire_event('updating')
                
            session.add(self)
            session.commit()
            
            if is_new:
                self.fire_event('created')
            else:
                self.fire_event('updated')
                
            self.fire_event('saved')
            return self
            
        except:
            session.rollback()
            raise
    
    def delete(self):
        """Supprime le modèle avec événements"""
        self.fire_event('deleting')
        
        session = self.get_session()
        try:
            if self._soft_deletes:
                self.deleted_at = datetime.now()
                session.add(self)
                session.commit()
            else:
                session.delete(self)
                session.commit()
            
            self.fire_event('deleted')
            return self
            
        except:
            session.rollback()
            raise
        
    @classmethod
    def with_(cls, *relations):
        """
        Crée une requête avec chargement eager des relations.
        
        Args:
            *relations: Relations à charger
                - str: Nom de la relation
                - callable: Configuration de la relation
        """
        query = cls.query()
        for relation in relations:
            if callable(relation):
                # Pour les relations avec des contraintes
                query = relation(query)
            else:
                # Pour les relations simples
                query = query.with_(relation)
        return query
        
    @classmethod
    def find(cls, id):
        """Find a model by its primary key."""
        return cls.query().find(id)
        
    @classmethod
    def where(cls, *args, **kwargs):
        """Add a basic where clause to the query."""
        return cls.query().where(*args, **kwargs)
    
    def to_pydantic(self) -> BaseModel:
        """Convertit le modèle en instance Pydantic."""
        if not self.Schema:
            fields = {
                column.key: (self._get_python_type(column.type), ...)
                for column in self.__table__.columns
            }
            schema_class = create_model(
                f'{self.__class__.__name__}Schema',
                __config__=type('Config', (), {'from_attributes': True}),
                **fields
            )
            return schema_class.model_validate(self)
            
        return self.Schema.model_validate(self)
        
    @classmethod
    def from_pydantic(cls: Type[T], schema: BaseModel) -> T:
        return cls(**schema.model_dump(exclude_unset=True))

    def belongs_to(self, related: str, foreign_key: str, owner_key: str = 'id') -> 'BelongsTo':
        """Crée une relation belongs_to"""
        from ..relations import BelongsTo
        from ..model.registry import ModelRegistry
        related_class = ModelRegistry.resolve(related)
        return BelongsTo(self, related_class, foreign_key, owner_key)
        
    def has_many(self, related: str, foreign_key: str, local_key: str = 'id') -> 'HasMany':
        """Crée une relation has_many"""
        from ..relations import HasMany
        from ..model.registry import ModelRegistry
        related_class = ModelRegistry.resolve(related)
        return HasMany(self, related_class, foreign_key, local_key)
        
    def has_one(self, related: str, foreign_key: str, local_key: str = 'id') -> 'HasOne':
        """Crée une relation has_one"""
        from ..relations import HasOne
        from ..model.registry import ModelRegistry
        related_class = ModelRegistry.resolve(related)
        return HasOne(self, related_class, foreign_key, local_key)

    def __getattr__(self, key: str) -> Any:
        """Gère l'accès aux attributs et relations"""
        # Vérifie d'abord les attributs castés
        if key in self._casts:
            value = self._attributes.get(key)
            return CastRegistry.cast(value, self._casts[key])
            
        # Vérifie les relations chargées
        if key in self._relations:
            return self._relations[key]
            
        # Vérifie les méthodes de relation
        if hasattr(self.__class__, key):
            method = getattr(self.__class__, key)
            if callable(method):
                relation = method(self)
                if key in self._loaded_relations:
                    result = relation.get_results()
                    self._relations[key] = result
                    return result
                return relation
                
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{key}'")
    
    def __setattr__(self, key: str, value: Any):
        """Gère l'assignation des attributs avec cast."""
        if key in self._casts:
            cast_class = CastRegistry.get(self._casts[key])
            if isinstance(cast_class, type) and issubclass(cast_class, Cast):
                value = cast_class().to_database(value)
        super().__setattr__(key, value)

    @classmethod
    def set_connection(cls, connection_or_url):
        """Configure la connexion à la base de données"""
        if isinstance(connection_or_url, str):
            engine = create_engine(connection_or_url)
        else:
            engine = connection_or_url
            
        cls._connection = engine
        cls._session_factory = sessionmaker(bind=engine)
        cls._session = scoped_session(cls._session_factory)
        
    @classmethod
    def get_session(cls):
        """Récupère la session courante"""
        if cls._session is None:
            raise RuntimeError("Database connection not configured. Call Model.set_connection() first.")
        return cls._session()
    
    @property
    def session(self):
        """Récupère la session pour l'instance"""
        return self.get_session()

    @classmethod
    def aggregate(cls) -> AggregateBuilder:
        return AggregateBuilder(cls)

    def __init_subclass__(cls) -> None:
        """Appelé quand une sous-classe est créée"""
        super().__init_subclass__()
        if not cls.__abstract__:
            ModelRegistry.add(cls.__name__, cls) 