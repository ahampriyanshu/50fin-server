import uuid
from .database import Base
import datetime
from sqlalchemy import Column, String, DateTime
from app.database import Base, engine
from sqlalchemy.dialects.postgresql import UUID

class Post(Base):
    __tablename__ = 'blogs'
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    title = Column(String, nullable=False, unique=True)
    body = Column(String, nullable=False)
    slug = Column(String, nullable=False, default='dsfsdfds')
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
Base.metadata.create_all(bind=engine, checkfirst=True)