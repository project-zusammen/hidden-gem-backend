"""empty message

Revision ID: c23917bdf59b
Revises: 1a1b4ba09824
Create Date: 2024-01-20 11:49:25.905318

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c23917bdf59b'
down_revision = '1a1b4ba09824'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('region',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('public_id', sa.String(length=100), nullable=True),
    sa.Column('city', sa.String(length=100), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('city'),
    sa.UniqueConstraint('public_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('region')
    # ### end Alembic commands ###
