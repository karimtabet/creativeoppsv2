from datetime import datetime

from sqlalchemy import MetaData, Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from markdown import markdown

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

    id = Column(String, primary_key=True)
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

    def __str__(self):
        return '{title}'.format(title=self.title)

    def as_dict(self):
        d = {'id': self.id,
             'title': self.title,
             'description': self.description,
             'location': self.location,
             'body': markdown(self.body),
             'datetime': self.datetime.strftime("%a, %d %b %Y"),
             'avatar_url': self.avatar_url}
        if len(self.images) > 0:
            d['images'] = [image.as_dict() for image in self.images]
        if len(self.images) > 0:
            d['videos'] = [video.as_dict() for video in self.videos]
        return d


class Image(Base):
    __tablename__ = 'images'

    image_url = Column(String, primary_key=True)
    project_id = Column(
        ForeignKey('projects.id'),
        primary_key=True,
        index=True
    )
    thumbnail_url = Column(String, nullable=False)

    def __repr__(self):
        return '<Image {url}>'.format(url=self.image_url)

    def as_dict(self):
        return {'image_url': self.image_url,
                'project_id': self.project_id,
                'thumbnail_url': self.thumbnail_url}


class Video(Base):
    __tablename__ = 'videos'

    video_url = Column(String, primary_key=True)
    project_id = Column(
        ForeignKey('projects.id'),
        primary_key=True,
        index=True
    )
    thumbnail_url = Column(String, nullable=False)

    def __repr__(self):
        return '<Video {url}>'.format(url=self.video_url)

    def as_dict(self):
        return {'video_url': self.video_url,
                'project_id': self.project_id,
                'thumbnail_url': self.thumbnail_url}


class Policy(Base):
    __tablename__ = 'policies'

    policy_uuid = Column(UUID(as_uuid=True), primary_key=True)
    heading = Column(String, nullable=False)
    body = Column(String, nullable=False)

    def as_dict(self):
        return {'heading': self.heading,
                'body': markdown(self.body)}


class IndexCarouselItem(Base):
    __tablename__ = 'index_carousel_items'

    uuid = Column(UUID(as_uuid=True), primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    image_url = Column(String, nullable=False)
    read_more_url = Column(String, nullable=False)


class IndexContent(Base):
    __tablename__ = 'index_content'

    uuid = Column(UUID(as_uuid=True), primary_key=True)

    feature_1_title = Column(String, nullable=False)
    feature_1_image_url = Column(String, nullable=False)
    feature_1_description = Column(String, nullable=False)
    feature_1_read_more_url = Column(String, nullable=False)

    feature_2_title = Column(String, nullable=False)
    feature_2_image_url = Column(String, nullable=False)
    feature_2_description = Column(String, nullable=False)
    feature_2_read_more_url = Column(String, nullable=False)

    feature_3_title = Column(String, nullable=False)
    feature_3_image_url = Column(String, nullable=False)
    feature_3_description = Column(String, nullable=False)
    feature_3_read_more_url = Column(String, nullable=False)

    mid_page_heading = Column(String, nullable=False)
    mid_page_text = Column(String, nullable=False)

    mid_page_feature_1_title = Column(String, nullable=False)
    mid_page_feature_1_image_url = Column(String, nullable=False)
    mid_page_feature_1_description = Column(String, nullable=False)

    mid_page_feature_2_title = Column(String, nullable=False)
    mid_page_feature_2_image_url = Column(String, nullable=False)
    mid_page_feature_2_description = Column(String, nullable=False)

    mid_page_feature_3_title = Column(String, nullable=False)
    mid_page_feature_3_image_url = Column(String, nullable=False)
    mid_page_feature_3_description = Column(String, nullable=False)

    latest_activity_image_1_url = Column(String, nullable=False)
    latest_activity_image_2_url = Column(String, nullable=False)
    latest_activity_image_3_url = Column(String, nullable=False)

    def as_dict(self):
        return {'feature_1_title': self.feature_1_title,
                'feature_1_image_url': self.feature_1_image_url,
                'feature_1_description': self.feature_1_description,
                'feature_1_read_more_url': self.feature_1_read_more_url,
                'feature_2_title': self.feature_2_title,
                'feature_2_image_url': self.feature_2_image_url,
                'feature_2_description': self.feature_2_description,
                'feature_2_read_more_url': self.feature_2_read_more_url,
                'feature_3_title': self.feature_3_title,
                'feature_3_image_url': self.feature_3_image_url,
                'feature_3_description': self.feature_3_description,
                'feature_3_read_more_url': self.feature_3_read_more_url,
                'mid_page_heading': self.mid_page_heading,
                'mid_page_text': markdown(self.mid_page_text),
                'mid_page_feature_1_title': self.mid_page_feature_1_title,
                'mid_page_feature_1_image_url': (
                    self.mid_page_feature_1_image_url),
                'mid_page_feature_1_description': (
                    self.mid_page_feature_1_description),
                'mid_page_feature_2_title': self.mid_page_feature_2_title,
                'mid_page_feature_2_image_url': (
                    self.mid_page_feature_2_image_url),
                'mid_page_feature_2_description': (
                    self.mid_page_feature_2_description),
                'mid_page_feature_3_title': self.mid_page_feature_3_title,
                'mid_page_feature_3_image_url': (
                    self.mid_page_feature_3_image_url),
                'mid_page_feature_3_description': (
                    self.mid_page_feature_3_description),
                'latest_activity_image_1_url': (
                    self.latest_activity_image_1_url),
                'latest_activity_image_2_url': (
                    self.latest_activity_image_2_url),
                'latest_activity_image_3_url': (
                    self.latest_activity_image_3_url)}
