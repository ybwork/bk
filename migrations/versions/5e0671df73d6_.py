"""empty message

Revision ID: 5e0671df73d6
Revises: 657250e26f86
Create Date: 2019-01-22 06:39:06.881879

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5e0671df73d6'
down_revision = '657250e26f86'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bank',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('balance', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bank')
    # ### end Alembic commands ###
