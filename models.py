from sqlalchemy import Column, Integer, String
from database import Base

class ToDoDB(Base):
    """
    Database model for To-Do items.
    """
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    task = Column(String, index=True)
