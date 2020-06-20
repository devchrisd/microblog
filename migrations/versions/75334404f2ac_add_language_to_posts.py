"""add language to posts

Revision ID: 75334404f2ac
Revises: ec4883ce776c
Create Date: 2020-06-17 17:36:53.378324

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '75334404f2ac'
down_revision = 'ec4883ce776c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('language', sa.String(length=5), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'language')
    # ### end Alembic commands ###
