"""empty message

Revision ID: fbb9450ded22
Revises: 3a9b7dcf9c84
Create Date: 2021-05-07 13:59:21.213582

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fbb9450ded22'
down_revision = '3a9b7dcf9c84'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Artist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('genres', sa.PickleType(), nullable=True),
    sa.Column('city', sa.String(length=120), nullable=False),
    sa.Column('state', sa.String(length=120), nullable=False),
    sa.Column('phone', sa.String(length=120), nullable=False),
    sa.Column('website', sa.String(length=120), nullable=True),
    sa.Column('facebook_link', sa.String(length=120), nullable=True),
    sa.Column('seeking_venue', sa.Boolean(), nullable=True),
    sa.Column('venue_description', sa.String(), nullable=True),
    sa.Column('image_link', sa.String(length=500), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('Show', sa.Column('artist_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'Show', 'Artist', ['artist_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'Show', type_='foreignkey')
    op.drop_column('Show', 'artist_id')
    op.drop_table('Artist')
    # ### end Alembic commands ###
