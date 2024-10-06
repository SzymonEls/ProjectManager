"""Project category

Revision ID: be4490db8225
Revises: 56ab4d989dc8
Create Date: 2024-09-21 18:54:00.142242

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be4490db8225'
down_revision = '56ab4d989dc8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('project', schema=None) as batch_op:
        batch_op.add_column(sa.Column('category', sa.String(length=255), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('project', schema=None) as batch_op:
        batch_op.drop_column('category')

    # ### end Alembic commands ###
