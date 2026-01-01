from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, unique=True, index=True)
    #image = Column(None)
    author_id = relationship(Integer, ForeignKey("users.id"))

    author = relationship("User", back_populates="posts")