"""empty message

Revision ID: ddbe492ae95f
Revises: 73305f628c4f
Create Date: 2023-04-13 16:47:01.217149

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ddbe492ae95f'
down_revision = '73305f628c4f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('movie', schema=None) as batch_op:
        batch_op.add_column(sa.Column('create_time', sa.DateTime(), nullable=False))

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('create_time', sa.DateTime(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('create_time')

    with op.batch_alter_table('movie', schema=None) as batch_op:
        batch_op.drop_column('create_time')

    # ### end Alembic commands ###
