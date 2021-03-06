"""empty message

Revision ID: 9919f61c435f
Revises: 695d60e74bcf
Create Date: 2021-08-05 16:29:35.656076

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9919f61c435f'
down_revision = '695d60e74bcf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_admin', sa.Boolean(), server_default=sa.text('false'), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'is_admin')

    # ### end Alembic commands ###
