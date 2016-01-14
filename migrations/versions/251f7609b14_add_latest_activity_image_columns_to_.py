"""add latest activity image columns to index content table

Revision ID: 251f7609b14
Revises: 33a75d55c5f
Create Date: 2016-01-14 20:19:31.031884

"""

# revision identifiers, used by Alembic.
revision = '251f7609b14'
down_revision = '33a75d55c5f'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('index_content', sa.Column('latest_activity_image_1_url', sa.String(), nullable=True))
    op.add_column('index_content', sa.Column('latest_activity_image_2_url', sa.String(), nullable=True))
    op.add_column('index_content', sa.Column('latest_activity_image_3_url', sa.String(), nullable=True))

    op.execute(sa.sql.text("update index_content set latest_activity_image_1_url = 'http://www.example.com'"))
    op.execute(sa.sql.text("update index_content set latest_activity_image_2_url = 'http://www.example.com'"))
    op.execute(sa.sql.text("update index_content set latest_activity_image_3_url = 'http://www.example.com'"))
    op.alter_column('index_content', "latest_activity_image_1_url", nullable=False)
    op.alter_column('index_content', "latest_activity_image_2_url", nullable=False)
    op.alter_column('index_content', "latest_activity_image_3_url", nullable=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('index_content', 'latest_activity_image_3_url')
    op.drop_column('index_content', 'latest_activity_image_2_url')
    op.drop_column('index_content', 'latest_activity_image_1_url')
    ### end Alembic commands ###
