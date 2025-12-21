"""added busy_day uc

Revision ID: b87f871635e6
Revises: 0472cb273c00
Create Date: 2025-12-21 17:35:20.142588

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "b87f871635e6"
down_revision = "0472cb273c00"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_unique_constraint("busy_date_uc", "busy_date", ["user_id", "date_"])


def downgrade() -> None:
    op.drop_constraint("busy_date_uc", "busy_date", type_="unique")
