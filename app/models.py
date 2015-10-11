from datetime import datetime

from sqlalchemy import MetaData, Column, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

convention = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s'
}

metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)


class Project(Base):
    __tablename__ = 'projects'

    project_uuid = Column(UUID(as_uuid=True), primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    location = Column(String, nullable=False)
    body = Column(String, nullable=False)
    datetime = Column(DateTime(timezone=True), nullable=False,
                      default=datetime.utcnow)
    avatar_url = Column(String, nullable=False)

    images = relationship("Image", backref="project")
    videos = relationship("Video", backref="project")

    def __repr__(self):
        return '<Project {title}>'.format(title=self.title)


class Image(Base):
    __tablename__ = 'images'

    image_url = Column(String, primary_key=True, nullable=False)
    thumbnail_url = Column(String, nullable=False)
    project_uuid = Column(
        ForeignKey('projects.project_uuid'),
        nullable=False,
        index=True
    )

    def __repr__(self):
        return '<Image {url}>'.format(url=self.image_url)


class Video(Base):
    __tablename__ = 'videos'

    video_url = Column(String, primary_key=True, nullable=False)
    thumbnail_url = Column(String, nullable=False)
    project_uuid = Column(
        ForeignKey('projects.project_uuid'),
        nullable=False,
        index=True
    )

    def __repr__(self):
        return '<Video {url}>'.format(url=self.video_url)
