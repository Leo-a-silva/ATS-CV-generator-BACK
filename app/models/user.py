from datetime import datetime
from sqlalchemy import Column, BigInteger, String, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from ..database import Base


class User(Base):
    __tablename__ = "User"
    id = Column(BigInteger, primary_key=True, index=True)
    email_address = Column(String(100), nullable=False, unique=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow
    )
    password_hash = Column(Text, nullable=False)

    cvs = relationship("Cv", back_populates="user")
