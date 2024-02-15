from db.models import NewsletterResources
from db.database import Session


class NewsletterUtils:
    def __init__(self):
        self.db = Session()

    def list_resources(self):
        try:
            resources = self.db.query(NewsletterResources).all()
            return resources
        finally:
            self.db.close()
