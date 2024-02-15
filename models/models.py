from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class NewsletterResources(Base):
    __tablename__ = 'newsletter_resources'
    id = Column(Integer, primary_key=True)
    url = Column(String(255), nullable=False)
