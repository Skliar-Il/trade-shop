"""empty message

Revision ID: b663a7e4a400
Revises: 14257614098f
Create Date: 2024-07-11 20:14:19.336019

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'b663a7e4a400'
down_revision: Union[str, None] = '14257614098f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('photo', sa.String(), nullable=True),
    sa.Column('date_published', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.Column('prise', sa.Float(), nullable=False),
    sa.Column('contacts', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('users')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('photo', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('date_published', postgresql.TIMESTAMP(), server_default=sa.text("timezone('utc'::text, now())"), autoincrement=False, nullable=False),
    sa.Column('prise', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('contacts', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='users_pkey')
    )
    op.drop_table('products')
    # ### end Alembic commands ###
