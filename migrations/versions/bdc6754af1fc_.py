"""empty message

Revision ID: bdc6754af1fc
Revises: f3dfbcac51e1
Create Date: 2023-12-23 13:13:24.263333

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "bdc6754af1fc"
down_revision = "f3dfbcac51e1"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("review", schema=None) as batch_op:
        batch_op.alter_column("upvotes", existing_type=mysql.INTEGER(), nullable=False)
        batch_op.alter_column(
            "downvotes", existing_type=mysql.INTEGER(), nullable=False
        )



def downgrade():
    with op.batch_alter_table("review", schema=None) as batch_op:
        batch_op.alter_column("downvotes", existing_type=mysql.INTEGER(), nullable=True)
        batch_op.alter_column("upvotes", existing_type=mysql.INTEGER(), nullable=True)

