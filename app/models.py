from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Text
from app.database import Base
from uuid import uuid4

class Identity(Base):
    __tablename__ = "identities"
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    email = Column(String, unique=True, nullable=False)

class Account(Base):
    __tablename__ = "accounts"
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    identity_id = Column(String, ForeignKey("identities.id"))
    service = Column(String)
    confidence = Column(Integer)
    confirmed = Column(Boolean, default=False)
    ignored = Column(Boolean, default=False)

class Signal(Base):
    __tablename__ = "signals"
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    account_id = Column(String, ForeignKey("accounts.id"))
    description = Column(Text)
