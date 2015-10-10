from flask.ext.testing import TestCase

from app import app, db
from app.models import Base


class CreativeOpportunitiesTestCase(TestCase):
    def create_app(self):
        return app

    def setUp(self):
        db.session.close()
        for table in reversed(Base.metadata.sorted_tables):
            db.session.execute(
                "delete from {table_name};"
                .format(table_name=table.name)
            )
