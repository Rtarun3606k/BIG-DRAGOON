"""added language coloum

Revision ID: dccf93efd4ee
Revises: e0b36daf25c4
Create Date: 2024-07-22 07:33:37.868099

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dccf93efd4ee'
down_revision = 'e0b36daf25c4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('program', schema=None) as batch_op:
        batch_op.add_column(sa.Column('program_language', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('program', schema=None) as batch_op:
        batch_op.drop_column('program_language')

    # ### end Alembic commands ###
