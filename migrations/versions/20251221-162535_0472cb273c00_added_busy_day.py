"""added busy_day

Revision ID: 0472cb273c00
Revises: 812049d3a1da
Create Date: 2025-12-21 16:25:35.131064

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "0472cb273c00"
down_revision = "812049d3a1da"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "busy_date",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column(
            "busy",
            sa.Boolean(),
            nullable=False,
            server_default=op.f("false"),
            default=lambda: False,
        ),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("date_", sa.Date(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("fk__busy_date__user_id__users")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__busy_date")),
    )


def downgrade() -> None:
    op.drop_table("busy_date")
