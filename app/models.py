from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.sql.expression import text

from .database import Base

class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, server_default='TRUE')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('CURRENT_TIMESTAMP'))

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    
