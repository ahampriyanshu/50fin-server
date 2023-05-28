import uuid
from .database import Base
import datetime
from slugify import slugify
from sqlalchemy import Column, String, Text, DateTime
from app.database import Base, engine
from sqlalchemy.dialects.postgresql import UUID


class Post(Base):
    __tablename__ = "blog"
    id = Column(
        UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4
    )
    title = Column(String(100), nullable=False)
    body = Column(Text, nullable=False)
    slug = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=None, onupdate=datetime.datetime.utcnow)

    def generate_slug(self):
        return slugify(self.title)


Base.metadata.create_all(bind=engine, checkfirst=True)
