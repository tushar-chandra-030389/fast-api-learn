from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

from .database import Base

class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, server_default='TRUE')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)

    owner = relationship('User')

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('CURRENT_TIMESTAMP'))

    def get_details(self):
        return { col.name: getattr(self, col.name) for col in self.__table__.columns if col.name != 'password' }
       
