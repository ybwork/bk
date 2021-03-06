"""empty message

Revision ID: 58496fbe6938
Revises: 
Create Date: 2019-01-26 10:00:56.958979

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '58496fbe6938'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('app',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('key', sa.String(length=16), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('key')
    )
    op.create_table('bank',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('balance', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('client',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('status_payment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('invoice',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('num', sa.String(length=5), nullable=False),
    sa.Column('balance', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.Column('bank_id', sa.Integer(), nullable=False),
    sa.Column('client_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['bank_id'], ['bank.id'], ),
    sa.ForeignKeyConstraint(['client_id'], ['client.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('payment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('key', sa.String(length=5), nullable=False),
    sa.Column('amount_money', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.Column('number_invoice_provider', sa.String(length=5), nullable=False),
    sa.Column('number_invoice_reciever', sa.String(length=5), nullable=False),
    sa.Column('code_confirm', sa.Integer(), nullable=True),
    sa.Column('status_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['status_id'], ['status_payment.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_payment_code_confirm'), 'payment', ['code_confirm'], unique=False)
    op.create_index(op.f('ix_payment_number_invoice_provider'), 'payment', ['number_invoice_provider'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_payment_number_invoice_provider'), table_name='payment')
    op.drop_index(op.f('ix_payment_code_confirm'), table_name='payment')
    op.drop_table('payment')
    op.drop_table('invoice')
    op.drop_table('status_payment')
    op.drop_table('client')
    op.drop_table('bank')
    op.drop_table('app')
    # ### end Alembic commands ###
