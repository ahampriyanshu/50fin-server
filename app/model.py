import uuid
from .database import Base
import datetime
from math import ceil
from utils.constants import WPM
from sqlalchemy import Column, String, Text, DateTime
from app.database import Base, engine
from sqlalchemy.dialects.postgresql import UUID

class Post(Base):
    __tablename__ = 'blogggg'
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    title = Column(String(100), nullable=False, unique=True)
    body = Column(Text, nullable=False)
    slug = Column(String, nullable=False, default='dsfsdfds')
    reading_time = Column(String(10))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=None, onupdate=datetime.datetime.utcnow)
    
    def calculate_reading_time(self):
        words = self.body.split()
        total_words = len(words)
        reading_time_minutes = ceil(total_words / WPM)
        self.reading_time = f"{reading_time_minutes} min"
    
Base.metadata.create_all(bind=engine, checkfirst=True)