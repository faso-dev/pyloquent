from typing import TypeVar
from ..relations.relation import Relation
from ..types import ModelType

T = TypeVar('T', bound=ModelType)

class HasOne(Relation[T]):
    """
    Implémente une relation one-to-one.
    
    Example:
        class User(Model):
            def profile(self):
                return self.has_one(Profile, 'user_id')
                
        # Création avec relation
        user = User.create({
            'name': 'John',
            'profile': {
                'bio': 'Developer',
                'twitter': '@john'
            }
        })
        
        # Mise à jour
        user.profile().update({
            'bio': 'Senior Developer'
        })
        
        # Requêtes avec conditions
        users = User.query()\
            .where_has('profile', lambda q:
                q.where('is_public', True)
            )\
            .get()
    """
    
    def update_or_create(self, attributes: dict, values: dict = None) -> T:
        """
        Met à jour un modèle existant ou en crée un nouveau.
        
        Args:
            attributes: Attributs pour trouver le modèle
            values: Valeurs à mettre à jour ou créer
            
        Example:
            profile = user.profile().update_or_create(
                {'type': 'personal'},
                {
                    'bio': 'Developer',
                    'twitter': '@john'
                }
            )
        """
        self.fire_event('updating_or_creating', attributes, values)
        
        instance = self.where(attributes).first()
        if instance:
            instance.update(values or {})
        else:
            instance = self.create({**attributes, **(values or {})})
            
        self.fire_event('updated_or_created', instance)
        return instance 