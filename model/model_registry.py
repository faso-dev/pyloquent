from typing import Dict, Type, TypeVar, List
from libs.pyloquent.exceptions import PyloquentException

T = TypeVar('T')

class ModelRegistry:
    """
    Registre global des modèles pour la résolution des relations polymorphiques.
    
    Example:
        # Enregistrement automatique
        @model_registry.register
        class Post(Model):
            pass
            
        # Enregistrement manuel
        model_registry.add('posts', Post)
        
        # Résolution
        model_class = model_registry.resolve('posts')
        post = model_class.find(1)
    """
    
    _models: Dict[str, Type[T]] = {}
    _aliases: Dict[str, str] = {}
    
    @classmethod
    def add(cls, name: str, model: Type[T], aliases: List[str] = None) -> None:
        """
        Ajoute un modèle au registre.
        
        Args:
            name: Nom unique du modèle
            model: Classe du modèle
            aliases: Aliases optionnels pour le modèle
            
        Example:
            model_registry.add('posts', Post, ['article', 'blog_post'])
        """
        cls._models[name] = model
        
        if aliases:
            for alias in aliases:
                cls._aliases[alias] = name
                
    @classmethod
    def resolve(cls, name: str) -> Type[T]:
        """
        Résout un modèle par son nom ou alias.
        
        Raises:
            PyloquentException: Si le modèle n'est pas trouvé
            
        Example:
            Post = model_registry.resolve('posts')
            Article = model_registry.resolve('article')  # Même classe que Post
        """
        # Vérifie les aliases
        if name in cls._aliases:
            name = cls._aliases[name]
            
        if name not in cls._models:
            raise PyloquentException(f"Model not found: {name}")
            
        return cls._models[name]
    
    @classmethod
    def register(cls, model: Type[T]) -> Type[T]:
        """
        Décorateur pour enregistrer un modèle.
        
        Example:
            @model_registry.register
            class Post(Model):
                pass
        """
        name = model.__name__.lower()
        cls.add(name, model)
        return model 