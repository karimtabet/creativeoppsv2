from hamcrest import assert_that, has_length

from app.app import db
from app.images import get_flickr_images
from app.models import Project
from app.tests.utils import CreativeOpportunitiesTestCase


class TestImages(CreativeOpportunitiesTestCase):
    def get_flickr_images(self):
        project = self.insert_n_projects(1)[0]

        get_flickr_images(
            '72157648806036881',
            project.id
        )
        project = db.session.query(Project).one()

        assert_that(
            project.images,
            has_length(28)
        )

    def test_get_duplicate_images(self):
        project = self.insert_n_projects(1)[0]

        get_flickr_images(
            '72157648806036881',
            project.id
        )
        get_flickr_images(
            '72157648806036881',
            project.id
        )
        project = db.session.query(Project).one()

        assert_that(
            project.images,
            has_length(28)
        )
