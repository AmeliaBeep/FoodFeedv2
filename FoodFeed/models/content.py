from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from FoodFeed.core.database import Base


class Content(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, unique=True, index=True)
    #image = Column(None)

    author = relationship("User", back_populates="posts")