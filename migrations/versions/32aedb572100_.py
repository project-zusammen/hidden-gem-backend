"""empty message

Revision ID: 32aedb572100
Revises: 4d036d291155
Create Date: 2024-03-08 17:29:56.489143

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '32aedb572100'
down_revision = '4d036d291155'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('image',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('url', sa.String(length=255), nullable=False),
    sa.Column('review_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['review_id'], ['review.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('report', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('status', sa.String(length=100), nullable=False))
        batch_op.create_foreign_key(None, 'user', ['user_id'], ['id'])

    with op.batch_alter_table('review', schema=None) as batch_op:
        batch_op.add_column(sa.Column('category_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('tag_id', sa.Integer(), nullable=True))
        batch_op.alter_column('title',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
        batch_op.create_foreign_key('fk_review_tag', 'tag', ['tag_id'], ['id'])
        batch_op.create_foreign_key('fk_review_category', 'category', ['category_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('review', schema=None) as batch_op:
        batch_op.drop_constraint('fk_review_category', type_='foreignkey')
        batch_op.drop_constraint('fk_review_tag', type_='foreignkey')
        batch_op.alter_column('title',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
        batch_op.drop_column('tag_id')
        batch_op.drop_column('category_id')

    with op.batch_alter_table('report', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('status')
        batch_op.drop_column('user_id')

    op.drop_table('image')
    # ### end Alembic commands ###