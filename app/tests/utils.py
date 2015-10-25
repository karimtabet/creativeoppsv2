from datetime import datetime

from flask.ext.testing import TestCase

from app.app import app, db
from app.models import Base, Project


class CreativeOpportunitiesTestCase(TestCase):
    def create_app(self):
        return app

    def setUp(self):
        db.session.close()
        for table in reversed(Base.metadata.sorted_tables):
            db.session.execute(table.delete())

    def insert_n_projects(self, n):
        projects = []
        for index in range(n):
            project = Project(
                id='test-project-{n}'.format(n=index),
                title='Test Project {n}'.format(n=index),
                description='This is a test project.',
                location='Some place nice',
                body='Test project stuff',
                datetime=datetime.utcnow(),
                avatar_url='http://lorempixel.com/400/200/'
            )
            db.session.add(project)
            projects.append(project)
        return projects
