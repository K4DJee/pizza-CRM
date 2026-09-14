"""add password column to users

Revision ID: e7b934f2366f
Revises: 
Create Date: 2026-09-05 11:47:59.922360

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'e7b934f2366f'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Просто добавляем колонку password в существующую таблицу
    # nullable=True, чтобы не ломать существующие строки (или False, если добавите default)
    op.add_column('users', sa.Column('password', sa.String(), nullable=True))

def downgrade() -> None:
    # При откате миграции просто удаляем эту колонку
    op.drop_column('users', 'password')