from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
project = Table('project', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('title', VARCHAR(length=240)),
    Column('description', VARCHAR(length=380)),
    Column('location', VARCHAR(length=240)),
    Column('body', VARCHAR(length=2048)),
    Column('date', VARCHAR(length=120)),
    Column('avatar_url', VARCHAR(length=380)),
    Column('album_url', VARCHAR(length=380)),
    Column('thumbnail_url', VARCHAR(length=380)),
    Column('video_url', VARCHAR(length=380)),
    Column('video2_url', VARCHAR(length=380)),
    Column('video3_url', VARCHAR(length=380)),
)

project = Table('project', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('title', String(length=240)),
    Column('description', String(length=380)),
    Column('location', String(length=240)),
    Column('body', String(length=2048)),
    Column('date', String(length=120)),
    Column('avatar_url', String(length=380)),
    Column('album_url', String(length=380)),
    Column('thumbnail_url', String(length=380)),
    Column('video_urls', String(length=2048)),
)

about = Table('about', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('about_us', String(length=4096)),
    Column('about_us_vid_url', String(length=380)),
    Column('about_us_vid_desc', String(length=60)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['project'].columns['video2_url'].drop()
    pre_meta.tables['project'].columns['video3_url'].drop()
    pre_meta.tables['project'].columns['video_url'].drop()
    post_meta.tables['project'].columns['video_urls'].create()
    post_meta.tables['about'].columns['about_us_vid_desc'].create()
    post_meta.tables['about'].columns['about_us_vid_url'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['project'].columns['video2_url'].create()
    pre_meta.tables['project'].columns['video3_url'].create()
    pre_meta.tables['project'].columns['video_url'].create()
    post_meta.tables['project'].columns['video_urls'].drop()
    post_meta.tables['about'].columns['about_us_vid_desc'].drop()
    post_meta.tables['about'].columns['about_us_vid_url'].drop()
