"""Add user group

Revision ID: a59f38a54b57
Revises: 58dd404deabb
Create Date: 2021-03-02 14:07:48.581125

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a59f38a54b57'
down_revision = '58dd404deabb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('group', sa.Enum('ALC', 'ANAP', 'GTA', 'SAPOR', name='usergroup'), nullable=False))
    op.create_index(op.f('ix_user_group'), 'user', ['group'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_group'), table_name='user')
    op.drop_column('user', 'group')
    # ### end Alembic commands ###