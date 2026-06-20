from sqlalchemy import Column, Integer, String, Text
from  database import Base

##blog table
class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)