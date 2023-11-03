"""add field password link nullable=false

Revision ID: 57640aa61f07
Revises: d4d6c5a45d22
Create Date: 2023-11-03 12:23:32.787370

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57640aa61f07'
down_revision = 'd4d6c5a45d22'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('linksmodel', 'password',
               existing_type=sa.VARCHAR(length=16),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('linksmodel', 'password',
               existing_type=sa.VARCHAR(length=16),
               nullable=True)
    # ### end Alembic commands ###