from typing import List, Type
from .interfaces import SeederInterface
from ..model import Model

class Seeder(SeederInterface):
    """
    Classe de base pour créer des seeders.
    
    Example:
        class UserSeeder(Seeder):
            def run(self):
                UserFactory().create_many(10)
                
                # Admin
                UserFactory().create(
                    name='Admin',
                    email='admin@example.com',
                    role='admin'
                )
                
        # Utilisation
        UserSeeder().run()
    """
    
    def run(self) -> None:
        """À surcharger dans les classes enfants"""
        raise NotImplementedError()
        
    def call(self, seeders: List[Type['Seeder']]) -> None:
        """Exécute d'autres seeders"""
        for seeder in seeders:
            seeder().run() 