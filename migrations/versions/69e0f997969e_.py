"""empty message

Revision ID: 69e0f997969e
Revises: a9c9b4bb783d
Create Date: 2019-01-25 11:03:31.746057

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '69e0f997969e'
down_revision = 'a9c9b4bb783d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_payment_code_confirm'), 'payment', ['code_confirm'], unique=False)
    op.drop_index('ix_payment_invoice_reciever', table_name='payment')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_payment_invoice_reciever', 'payment', ['invoice_reciever'], unique=False)
    op.drop_index(op.f('ix_payment_code_confirm'), table_name='payment')
    # ### end Alembic commands ###