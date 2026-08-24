from sqlalchemy import Integer, Column, String, Boolean, Text, DateTime, func
from app.core.database import Base

class TaskModel(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(Text(300), nullable=True)
    is_done = Column(Boolean, default=False, nullable=False)
    
    create_date = Column(DateTime, server_default=func.now())
    update_date = Column(DateTime, server_default=func.now(), server_onupdate=func.now())