"""empty message

Revision ID: 0f45d78c59fc
Revises: 
Create Date: 2023-12-23 08:08:47.448484

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0f45d78c59fc"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "review",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("public_id", sa.String(length=100), nullable=True),
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.Column("content", sa.String(length=255), nullable=False),
        sa.Column("location", sa.String(length=100), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("upvotes", sa.Integer(), nullable=True),
        sa.Column("downvotes", sa.Integer(), nullable=True),
        sa.Column("visible", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("public_id"),
    )


def downgrade():
    op.drop_table("review")
