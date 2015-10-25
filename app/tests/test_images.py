from hamcrest import assert_that, has_length, contains_inanyorder

from app.app import db
from app.images import get_images_by_project, get_flickr_images
from app.models import Project, Image
from app.tests.utils import CreativeOpportunitiesTestCase


class TestImages(CreativeOpportunitiesTestCase):
    def test_get_images_by_project(self):
        projects = self.insert_n_projects(2)
        image_urls = [
            'http://oi44.tinypic.com/vcwcol.jpg',
            'http://oi49.tinypic.com/iwn242.jpg',
            'http://oi43.tinypic.com/16lwvbo.jpg',
            'http://oi43.tinypic.com/118zr6h.jpg'
        ]
        for url in image_urls[:2]:
            image = Image(
                image_url=url,
                thumbnail_url=url,
                project_id=projects[0].id
            )
            db.session.add(image)

        for url in image_urls[2:]:
            image = Image(
                image_url=url,
                thumbnail_url=url,
                project_id=projects[1].id
            )
            db.session.add(image)

        assert_that(
            get_images_by_project(projects[0].id),
            contains_inanyorder(*projects[0].images)
        )

        assert_that(
            get_images_by_project(projects[1].id),
            contains_inanyorder(*projects[1].images)
        )

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
