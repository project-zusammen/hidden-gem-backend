"""empty message

Revision ID: 556f4fee7f4a
Revises: ab41090f534b
Create Date: 2024-01-28 21:45:41.363626

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "556f4fee7f4a"
down_revision = "7b653f89a4fd"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.alter_column(
            "role",
            existing_type=postgresql.ENUM("admin", "user", name="userrole"),
            type_=sa.String(length=100),
            existing_nullable=False,
        )
        batch_op.alter_column(
            "status",
            existing_type=postgresql.ENUM("active", "inactive", name="userstatus"),
            type_=sa.String(length=100),
            existing_nullable=False,
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.alter_column(
            "status",
            existing_type=sa.String(length=100),
            type_=postgresql.ENUM("active", "inactive", name="userstatus"),
            existing_nullable=False,
        )
        batch_op.alter_column(
            "role",
            existing_type=sa.String(length=100),
            type_=postgresql.ENUM("admin", "user", name="userrole"),
            existing_nullable=False,
        )

    # ### end Alembic commands ###
