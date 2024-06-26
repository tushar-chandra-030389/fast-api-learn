"""Votes

Revision ID: 344dfec973c9
Revises: 0c3cf215d9fa
Create Date: 2024-06-09 11:39:34.183358

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '344dfec973c9'
down_revision: Union[str, None] = '0c3cf215d9fa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post_2')
    op.drop_table('user_2')
    op.drop_table('product')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('product',
    sa.Column('name', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('price', sa.REAL(), autoincrement=False, nullable=False),
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('is_sale', sa.BOOLEAN(), server_default=sa.text('false'), autoincrement=False, nullable=True),
    sa.Column('inventory', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('added_on', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='product_pkey')
    )
    op.create_table('user_2',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('user_2_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('email', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('password', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='user_2_pkey'),
    sa.UniqueConstraint('email', name='user_2_email_key'),
    postgresql_ignore_search_path=False
    )
    op.create_table('post_2',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('content', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user_2.id'], name='fk_post_user_id', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='post_2_pkey')
    )
    # ### end Alembic commands ###
