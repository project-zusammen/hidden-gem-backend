"""empty message

Revision ID: e10c1de7484d
Revises: bb7cb6913a68
Create Date: 2024-01-30 04:07:28.207048

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e10c1de7484d'
down_revision = 'bb7cb6913a68'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('appeal',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('public_id', sa.String(length=100), nullable=False),
    sa.Column('reason', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('status', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('public_id')
    )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    op.create_table('report',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('public_id', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('type', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('item_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('reason', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['item_id'], ['review.id'], name='report_item_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='report_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='report_pkey'),
    sa.UniqueConstraint('public_id', name='report_public_id_key')
    )
    op.drop_table('appeal')
    # ### end Alembic commands ###
