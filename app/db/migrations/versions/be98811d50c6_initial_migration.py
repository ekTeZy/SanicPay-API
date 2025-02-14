"""Initial migration

Revision ID: be98811d50c6
Revises: 55ff3ed19789
Create Date: 2025-02-13 20:57:18.942390

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'be98811d50c6'
down_revision: Union[str, None] = '55ff3ed19789'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('api_token', sa.String(), nullable=True))
    op.create_unique_constraint(None, 'users', ['api_token'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'api_token')
    # ### end Alembic commands ###
