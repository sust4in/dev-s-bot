from db.models import NewsletterResources
from db.database import engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

Session = sessionmaker(bind=engine)


class NewsletterUtils:
    def __init__(self):
        self.session = Session()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    def get_resources(self):
        try:
            resources = self.session.query(NewsletterResources).all()
            return {'status': 'ok', 'data': resources}
        except SQLAlchemyError as e:
            return {'status': 'error', 'message': f'An error occurred: {str(e)}'}

    def create_resource(self, url):
        if self.url_exists(url):
            return {'status': 'error', 'message': 'URL already exists in the database!'}

        try:
            new_resource = NewsletterResources(url=url)
            self.session.add(new_resource)
            self.session.commit()
            return {'status': 'ok', 'message': 'Resource added successfully!'}
        except SQLAlchemyError as e:
            self.session.rollback()
            return {'status': 'error', 'message': f'An error occurred: {str(e)}'}

    def update_resource(self, resource_id, new_url):
        if self.url_exists(new_url):
            return {'status': 'error', 'message': 'URL already exists in the database!'}

        try:
            resource = self.session.query(NewsletterResources).filter(NewsletterResources.id == resource_id).first()
            if resource:
                resource.url = new_url
                self.session.commit()
                return {'status': 'ok', 'message': 'Resource updated successfully!'}
            else:
                return {'status': 'error', 'message': 'Resource not found!'}
        except SQLAlchemyError as e:
            self.session.rollback()
            return {'status': 'error', 'message': f'An error occurred: {str(e)}'}

    def delete_resource(self, resource_id):
        try:
            resource = self.session.query(NewsletterResources).filter(NewsletterResources.id == resource_id).first()
            if resource:
                self.session.delete(resource)
                self.session.commit()
                return {'status': 'ok', 'message': 'Resource deleted successfully!'}
            else:
                return {'status': 'error', 'message': 'Resource not found!'}
        except SQLAlchemyError as e:
            self.session.rollback()
            return {'status': 'error', 'message': f'An error occurred: {str(e)}'}

    def url_exists(self, url):
        return self.session.query(NewsletterResources).filter(NewsletterResources.url == url).first() is not None
