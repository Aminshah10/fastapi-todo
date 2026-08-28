from sqlalchemy import Integer, Column, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from app.core.database import Base
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(20), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    created_date = Column(DateTime, server_default=func.now())
    updated_date = Column(
        DateTime, server_default=func.now(), server_onupdate=func.now()
    )

    tasks = relationship("TaskModel", back_populates="user")
    refresh_tokens = relationship("RefreshTokenModel", back_populates="user")

    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password)

    def set_password(self, password: str) -> None:
        self.password = self.hash_password(password)
