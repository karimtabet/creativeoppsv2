from hamcrest import assert_that, is_, has_length

from app.app import db
from app.videos import get_youtube_videos
from app.models import Project
from app.tests.utils import CreativeOpportunitiesTestCase


class TestVideos(CreativeOpportunitiesTestCase):
    def test_get_youtube_video(self):
        project = self.insert_n_projects(1)[0]

        get_youtube_videos(
            'https://www.youtube.com/watch?v=Lbjru5CQIW4',
            project.id
        )
        project = db.session.query(Project).first()

        assert_that(
            project.videos,
            has_length(1)
        )

        assert_that(
            project.videos[0].video_url,
            is_('https://www.youtube.com/watch?v=Lbjru5CQIW4')
        )

        assert_that(
            project.videos[0].thumbnail_url,
            is_('http://img.youtube.com/vi/Lbjru5CQIW4/maxresdefault.jpg')
        )

    def test_get_3_youtube_videos(self):
        project = self.insert_n_projects(1)[0]

        get_youtube_videos(
            'https://www.youtube.com/watch?v=Lbjru5CQIW4,'
            'https://www.youtube.com/watch?v=VEMWyBWw0cA,'
            'https://www.youtube.com/watch?v=7Ny-D2MCAfg',
            project.id
        )
        project = db.session.query(Project).one()

        assert_that(
            project.videos,
            has_length(3)
        )

    def test_get_duplicate_video(self):
        project = self.insert_n_projects(1)[0]

        get_youtube_videos(
            'https://www.youtube.com/watch?v=Lbjru5CQIW4,'
            'https://www.youtube.com/watch?v=Lbjru5CQIW4,'
            'https://www.youtube.com/watch?v=Lbjru5CQIW4',
            project.id
        )
        project = db.session.query(Project).one()

        assert_that(
            project.videos,
            has_length(1)
        )
