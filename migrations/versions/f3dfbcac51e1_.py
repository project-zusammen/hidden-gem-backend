"""empty message

Revision ID: f3dfbcac51e1
Revises: 0f45d78c59fc
Create Date: 2023-12-23 10:38:02.698983

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "f3dfbcac51e1"
down_revision = "0f45d78c59fc"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "review", "public_id", existing_type=mysql.VARCHAR(length=100), nullable=False
    )


def downgrade():
    op.alter_column(
        "review", "public_id", existing_type=mysql.VARCHAR(length=100), nullable=True
    )
