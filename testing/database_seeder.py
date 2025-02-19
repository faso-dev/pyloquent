from typing import List, Type
from .seeder import Seeder

class DatabaseSeeder(Seeder):
    """
    Seeder principal qui orchestre tous les autres seeders.
    
    Example:
        class DatabaseSeeder(Seeder):
            def run(self):
                self.call([
                    UserSeeder,
                    PostSeeder,
                    CommentSeeder
                ])
    """
    
    seeders: List[Type[Seeder]] = []
    
    def run(self) -> None:
        """Exécute tous les seeders enregistrés"""
        self.call(self.seeders) 