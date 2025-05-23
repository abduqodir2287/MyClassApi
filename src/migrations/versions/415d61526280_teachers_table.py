"""Teachers table

Revision ID: 415d61526280
Revises: 3026b74fb0df
Create Date: 2025-02-12 23:12:02.873393

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '415d61526280'
down_revision: Union[str, None] = '3026b74fb0df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('teachers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('firstname', sa.String(), nullable=True),
    sa.Column('lastname', sa.String(), nullable=True),
    sa.Column('photo_url', sa.String(), nullable=True),
    sa.Column('birthDate', sa.String(), nullable=True),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('subject', sa.String(), nullable=True),
    sa.Column('idol', sa.String(), nullable=True),
    sa.Column('bio', sa.String(), nullable=True),
    sa.Column('social_link', sa.String(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.add_column('students', sa.Column('bio', sa.String(), nullable=True))
    op.add_column('students', sa.Column('social_link', sa.String(), nullable=True))
    op.drop_column('students', 'social_network')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('students', sa.Column('social_network', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('students', 'social_link')
    op.drop_column('students', 'bio')
    op.drop_table('teachers')
    # ### end Alembic commands ###
