"""Add foreign key to post table


Revision ID: 0c3cf215d9fa
Revises: 66068488008e
Create Date: 2024-06-09 11:21:44.917871

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0c3cf215d9fa'
down_revision: Union[str, None] = '66068488008e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'post_2',
        sa.Column('user_id', sa.Integer(), nullable=False)
    )
    op.create_foreign_key('fk_post_user_id', 'post_2', 'user_2', ['user_id'], ['id'], ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint('fk_post_user_id', table_name='post2')
    op.drop_column('post_2', 'user_id')
