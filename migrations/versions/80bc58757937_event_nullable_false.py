"""event nullable false

Revision ID: 80bc58757937
Revises: 12a220bcc64a
Create Date: 2024-08-12 21:27:06.250531

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '80bc58757937'
down_revision = '12a220bcc64a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.alter_column('project_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('start',
               existing_type=sa.DATETIME(),
               nullable=False)
        batch_op.alter_column('end',
               existing_type=sa.DATETIME(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.alter_column('end',
               existing_type=sa.DATETIME(),
               nullable=True)
        batch_op.alter_column('start',
               existing_type=sa.DATETIME(),
               nullable=True)
        batch_op.alter_column('project_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###
