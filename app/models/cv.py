from datetime import datetime
from sqlalchemy import Column, BigInteger, String, Text, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from ..database import Base


class Cv(Base):
    __tablename__ = "Cv"
    id = Column(BigInteger, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email_address = Column(String(150), nullable=True)
    phone_number = Column(BigInteger, nullable=False)
    linkedin_url = Column(Text, nullable=False)
    portfolio_url = Column(Text, nullable=False)
    country = Column(String(80), nullable=False)
    city = Column(String(80), nullable=False)
    summary = Column(Text, nullable=False)
    updated_at = Column(
        TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow
    )
    user_id = Column(BigInteger, ForeignKey("User.id"), nullable=False)

    user = relationship("User", back_populates="cvs")
