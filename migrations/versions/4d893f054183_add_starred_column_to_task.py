"""add starred column to task

Revision ID: 4d893f054183
Revises: be4490db8225
Create Date: 2024-10-23 12:51:47.144067

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4d893f054183'
down_revision = 'be4490db8225'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('starred', sa.Boolean(), server_default='0', nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.drop_column('starred')

    # ### end Alembic commands ###
