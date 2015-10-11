"""creare project, image and video tables

Revision ID: 5123db1b41a
Revises: 
Create Date: 2015-10-11 21:50:53.411089

"""

# revision identifiers, used by Alembic.
revision = '5123db1b41a'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('projects',
    sa.Column('project_uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('location', sa.String(), nullable=False),
    sa.Column('body', sa.String(), nullable=False),
    sa.Column('datetime', sa.DateTime(timezone=True), nullable=False),
    sa.Column('avatar_url', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('project_uuid', name=op.f('pk_projects'))
    )
    op.create_table('images',
    sa.Column('image_url', sa.String(), nullable=False),
    sa.Column('thumbnail_url', sa.String(), nullable=False),
    sa.Column('project_uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['project_uuid'], ['projects.project_uuid'], name=op.f('fk_images_project_uuid_projects')),
    sa.PrimaryKeyConstraint('image_url', name=op.f('pk_images'))
    )
    op.create_index(op.f('ix_images_project_uuid'), 'images', ['project_uuid'], unique=False)
    op.create_table('videos',
    sa.Column('video_url', sa.String(), nullable=False),
    sa.Column('thumbnail_url', sa.String(), nullable=False),
    sa.Column('project_uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['project_uuid'], ['projects.project_uuid'], name=op.f('fk_videos_project_uuid_projects')),
    sa.PrimaryKeyConstraint('video_url', name=op.f('pk_videos'))
    )
    op.create_index(op.f('ix_videos_project_uuid'), 'videos', ['project_uuid'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_videos_project_uuid'), table_name='videos')
    op.drop_table('videos')
    op.drop_index(op.f('ix_images_project_uuid'), table_name='images')
    op.drop_table('images')
    op.drop_table('projects')
    ### end Alembic commands ###
