from hamcrest import assert_that, is_

from app.app import db
from app.flickr import get_pictures
from app.models import Image
from app.tests.utils import CreativeOpportunitiesTestCase


class TestFlickr(CreativeOpportunitiesTestCase):
    def test_get_pictures(self):
        project = self.insert_n_projects(1)[0]

        get_pictures(
            'https://www.flickr.com/photos/128639640@N03/'
            'sets/72157648806036881/',
            project.project_uuid
        )
        pictures = db.session.query(Image).all()

        assert_that(
            len(pictures),
            is_(1)
        )
