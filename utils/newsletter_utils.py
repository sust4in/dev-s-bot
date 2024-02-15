from models.models import NewsletterResources
from main import Session


class NewsletterUtils:
    def __init__(self):
        self.session = Session()

    def list_resources(self):
        resources = self.session.query(NewsletterResources).all()
        return resources
