from typing import Any, Type, TypeVar, Optional, Union, List
from libs.pyloquent.model.model import Model
from libs.pyloquent.resources.resource import Resource
from libs.pyloquent.resources.resource_collection import ResourceCollection
from libs.pyloquent.exceptions import RelationNotLoadedException

T = TypeVar('T', bound=Model)

class RelationshipFields:
    """
    Mixin to handle relationships in Resources.
    
    Example:
        class UserResource(Resource):
            def to_dict(self):
                return {
                    'id': self.model.id,
                    'name': self.model.name,
                    
                    # Relation simple
                    'profile': self.relation('profile', ProfileResource),
                    
                    # Relation avec transformation
                    'posts': self.relation('posts', PostResource, lambda posts:
                        posts.filter(lambda p: p.is_published)
                    ),
                    
                    # Relation avec métadonnées
                    'comments': self.relation_with_meta('comments', CommentResource, {
                        'count': lambda comments: len(comments),
                        'last_activity': lambda comments: max(c.created_at for c in comments)
                    }),
                    
                    # Relation imbriquée
                    'company': self.relation('company', CompanyResource, include=[
                        'address',
                        'employees' => EmployeeResource
                    ])
                }
    """
    
    def relation(
        self,
        name: str,
        resource: Type[Resource],
        transformer: Optional[callable] = None,
        include: List[str] = None
    ) -> Any:
        """
        Handle a relationship with optional transformation.
        
        Args:
            name: Name of the relation
            resource: Resource to use
            transformer: Optional transformation function
            include: Relations to include
            
        Example:
            'posts': self.relation('posts', PostResource, 
                lambda posts: posts.filter(lambda p: p.is_published)
            )
        """
        if not hasattr(self.model, name):
            raise RelationNotLoadedException(name, self.model.__class__.__name__)
            
        related = getattr(self.model, name)
        
        if related is None:
            return None
            
        if transformer:
            related = transformer(related)
            
        if isinstance(related, list):
            return resource.collection(related).to_dict()['data']
            
        return resource(related).to_dict()
        
    def relation_with_meta(
        self,
        name: str,
        resource: Type[Resource],
        meta: dict
    ) -> dict:
        """
        Handle a relationship with metadata.
        
        Args:
            name: Name of the relation
            resource: Resource to use
            meta: Dictionary of metadata with callables
            
        Example:
            'comments': self.relation_with_meta('comments', CommentResource, {
                'count': lambda comments: len(comments),
                'has_new': lambda comments: any(c.is_unread for c in comments)
            })
        """
        if not hasattr(self.model, name):
            raise RelationNotLoadedException(name, self.model.__class__.__name__)
            
        related = getattr(self.model, name)
        
        result = {
            'data': resource.collection(related).to_dict()['data'] if related else []
        }
        
        if meta:
            result['meta'] = {
                key: callback(related) if related else None
                for key, callback in meta.items()
            }
            
        return result
    
    def nested_relation(
        self,
        name: str,
        resource: Type[Resource],
        nested: List[Union[str, dict]]
    ) -> dict:
        """
        Handle a relationship with nested relations.
        
        Args:
            name: Name of the relation
            resource: Resource to use
            nested: List of relations to include
            
        Example:
            'company': self.nested_relation('company', CompanyResource, [
                'address',
                {'employees': EmployeeResource}
            ])
        """
        if not hasattr(self.model, name):
            raise RelationNotLoadedException(name, self.model.__class__.__name__)
            
        related = getattr(self.model, name)
        if not related:
            return None
            
        resource_instance = resource(related)
        
        for relation in nested:
            if isinstance(relation, str):
                resource_instance.load_relation(relation)
            elif isinstance(relation, dict):
                for rel_name, rel_resource in relation.items():
                    resource_instance.load_relation(rel_name, rel_resource)
                    
        return resource_instance.to_dict() 