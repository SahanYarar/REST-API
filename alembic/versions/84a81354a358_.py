"""empty message

Revision ID: 84a81354a358
Revises: d86b81f69adf
Create Date: 2021-08-16 18:11:22.292173

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import func

# revision identifiers, used by Alembic.
revision = '84a81354a358'
down_revision = 'ba74b9a6b8f7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True,server_default=func.now()))
    op.alter_column('users', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=True,server_default=func.now())
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'created_at',
               existing_type=sa.DateTime(timezone=True),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=True)
    op.drop_column('users', 'updated_at')
    # ### end Alembic commands ###
