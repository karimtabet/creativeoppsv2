from hamcrest import assert_that, is_

from app import db
from app.flickr import get_pictures
from app.models import Picture
from app.tests.utils import CreativeOpportunitiesTestCase


class TestFlickr(CreativeOpportunitiesTestCase):
    def test_get_pictures(self):
        get_pictures(
            'https://www.flickr.com/photos/128639640@N03/'
            'sets/72157648806036881/',
            1
        )
        pictures = db.session.query(Picture).all()

        assert_that(
            len(pictures),
            is_(1)
        )
