"""add default for field password link

Revision ID: 4f1371890ca9
Revises: 57640aa61f07
Create Date: 2023-11-03 12:32:25.333882

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '4f1371890ca9'
down_revision = '57640aa61f07'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('linksmodel', 'password',
               existing_type=sa.VARCHAR(length=16),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('linksmodel', 'password',
               existing_type=sa.VARCHAR(length=16),
               nullable=False)
    # ### end Alembic commands ###
