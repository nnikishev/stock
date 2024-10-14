"""empty message

Revision ID: 43f9b11d3939
Revises: 
Create Date: 2024-10-14 13:17:32.476697

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '43f9b11d3939'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('carousel',
    sa.Column('uuid', sa.UUID(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('image', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_table('products',
    sa.Column('uuid', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('attachments', sa.JSON(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('properties', sa.JSON(), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_table('settings',
    sa.Column('uuid', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('value', sa.String(), nullable=True),
    sa.Column('additional', sa.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('uuid')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('settings')
    op.drop_table('products')
    op.drop_table('carousel')
    # ### end Alembic commands ###