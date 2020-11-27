"""empty message

Revision ID: e0d96b1ee623
Revises: 4fca6309f014
Create Date: 2020-11-28 00:52:22.425119

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e0d96b1ee623'
down_revision = '4fca6309f014'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('stat_post', sa.Column('count', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('stat_post', 'count')
    # ### end Alembic commands ###