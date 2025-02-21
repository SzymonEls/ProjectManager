"""Add location and travel_time cloumns to Event table

Revision ID: b0fea1968e3f
Revises: a4f44813a6b6
Create Date: 2025-01-01 16:33:24.183496

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b0fea1968e3f'
down_revision = 'a4f44813a6b6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.add_column(sa.Column('location', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('travel_time', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.drop_column('travel_time')
        batch_op.drop_column('location')

    # ### end Alembic commands ###
