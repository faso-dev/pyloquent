from typing import Any, Dict, List, Optional, Union
from alembic import op
import sqlalchemy as sa
from .interfaces import MigrationInterface, TableOperation
from .column import Column

class Migration(MigrationInterface):
    """
    Helper pour les migrations Alembic.
    
    Example:
        def upgrade():
            Migration.create_table(
                'users',
                columns={
                    'id': Column.integer('id').primary_key(),
                    'name': Column.string('name', 100).nullable(False),
                    'email': Column.string('email').unique(),
                    'settings': Column.json('settings'),
                },
                timestamps=True
            )
            
        def downgrade():
            Migration.drop_table('users')
    """
    
    @classmethod
    def create_table(
        cls,
        name: str,
        columns: Dict[str, sa.Column],
        timestamps: bool = True,
        soft_deletes: bool = False,
        **options: Any
    ) -> None:
        """
        Crée une nouvelle table.
        
        Args:
            name: Nom de la table
            columns: Définition des colonnes
            timestamps: Ajouter created_at/updated_at
            soft_deletes: Ajouter deleted_at
            **options: Options supplémentaires
        """
        if timestamps:
            columns.update({
                'created_at': Column.datetime('created_at'),
                'updated_at': Column.datetime('updated_at')
            })
            
        if soft_deletes:
            columns['deleted_at'] = Column.datetime('deleted_at').nullable()
            
        op.create_table(name, *columns.values(), **options)
        
    @classmethod
    def alter_table(
        cls,
        name: str,
        add_columns: Optional[Dict[str, sa.Column]] = None,
        drop_columns: Optional[List[str]] = None,
        rename_columns: Optional[Dict[str, str]] = None,
        **options: Any
    ) -> None:
        """
        Modifie une table existante.
        
        Example:
            Migration.alter_table(
                'users',
                add_columns={
                    'phone': Column.string('phone'),
                },
                drop_columns=['old_field'],
                rename_columns={'email': 'email_address'}
            )
        """
        with op.batch_alter_table(name, **options) as batch_op:
            if add_columns:
                for column in add_columns.values():
                    batch_op.add_column(column)
                    
            if drop_columns:
                for column in drop_columns:
                    batch_op.drop_column(column)
                    
            if rename_columns:
                for old, new in rename_columns.items():
                    batch_op.alter_column(old, new_column_name=new)
                    
    @classmethod
    def drop_table(cls, name: str) -> None:
        """Supprime une table."""
        op.drop_table(name)
        
    @classmethod
    def rename_table(cls, old: str, new: str) -> None:
        """Renomme une table."""
        op.rename_table(old, new)
        
    @classmethod
    def add_foreign_key(
        cls,
        table: str,
        column: str,
        referenced_table: str,
        referenced_column: str = 'id',
        **options: Any
    ) -> None:
        """
        Ajoute une clé étrangère.
        
        Example:
            Migration.add_foreign_key(
                'posts', 'user_id',
                'users', 'id',
                ondelete='CASCADE'
            )
        """
        op.create_foreign_key(
            f"fk_{table}_{column}",
            table,
            referenced_table,
            [column],
            [referenced_column],
            **options
        ) 