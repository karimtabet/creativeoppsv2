from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
about = Table('about', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('about_us', VARCHAR(length=4096)),
    Column('about_us_vid_desc', VARCHAR(length=60)),
    Column('about_us_vid_url', VARCHAR(length=380)),
)

about = Table('about', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('about_us', String(length=4096)),
    Column('about_us_vid_url', String(length=380)),
    Column('about_us_vid_caption', String(length=60)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['about'].columns['about_us_vid_desc'].drop()
    post_meta.tables['about'].columns['about_us_vid_caption'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['about'].columns['about_us_vid_desc'].create()
    post_meta.tables['about'].columns['about_us_vid_caption'].drop()
