"""fix role column to string

Revision ID: 8e9db5833b39
Revises: 
Create Date: 2026-09-15 14:31:06.510427

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8e9db5833b39'
down_revision = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    
    # Создаём новую колонку role как String
    op.add_column(
        'users',
        sa.Column(
            'role',
            sa.String(20),
            nullable=False,
            server_default='customer'
        )
    )
    
    # Добавляем check constraint
    op.create_check_constraint(
        'check_role',
        'users',
        "role IN ('customer', 'kitchen', 'admin')"
    )


def downgrade() -> None:
    op.drop_constraint('check_role', 'users', type_='check')
    op.drop_column('users', 'role')