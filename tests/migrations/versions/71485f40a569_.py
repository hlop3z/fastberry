"""empty message

Revision ID: 71485f40a569
Revises: 
Create Date: 2022-11-27 22:52:42.848655

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '71485f40a569'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('todo_task',
    sa.Column('_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('status', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('todo_task')
    # ### end Alembic commands ###
