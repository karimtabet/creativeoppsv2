from hamcrest import assert_that, has_length

from app.app import db
from app.flickr import get_pictures
from app.models import Project
from app.tests.utils import CreativeOpportunitiesTestCase


class TestFlickr(CreativeOpportunitiesTestCase):
    def test_get_pictures(self):
        project = self.insert_n_projects(1)[0]

        get_pictures(
            '72157648806036881',
            project.project_uuid
        )
        project = db.session.query(Project).one()

        assert_that(
            project.images,
            has_length(28)
        )
