"""empty message

Revision ID: 02f4cab2ba51
Revises: 9919f61c435f
Create Date: 2021-08-11 16:10:23.195440

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '02f4cab2ba51'
down_revision = '9919f61c435f'
branch_labels = None
depends_on = None


def upgrade():

    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('new_name', sa.String(length=80), server_default='adana', nullable=True))
    # ### end Alembic commands ###


def downgrade():

    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'new_name')
    # ### end Alembic commands ###
