"""Add content column to post table

Revision ID: 27af9c18b4ca
Revises: 0825753cf8db
Create Date: 2024-06-09 00:48:18.980539

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '27af9c18b4ca'
down_revision: Union[str, None] = '0825753cf8db'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'post_2',
        sa.Column('content', sa.String(), nullable=False ) 
    )


def downgrade() -> None:
    op.drop_column('post_2', 'content')
