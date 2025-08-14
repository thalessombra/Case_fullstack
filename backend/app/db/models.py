from sqlalchemy import Column, Integer, String, Boolean, Date, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    email = Column(String(200), unique=True, nullable=False)     
    is_active = Column(Boolean, default=True)
    
    allocations = relationship("Allocation", back_populates="client")


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(20), unique=True, nullable=False)
    name = Column(String(200), nullable=True)

    
    daily_returns = relationship("DailyReturn", back_populates="asset", cascade="all, delete-orphan")


class Allocation(Base):
    __tablename__ = "allocations"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    qty = Column(Numeric, nullable=False)
    price = Column(Numeric, nullable=False)
    bought_at = Column(Date, nullable=False)

    client = relationship("Client", back_populates="allocations")
    asset = relationship("Asset", back_populates="allocations")


class DailyReturn(Base):
    __tablename__ = "daily_returns"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    date = Column(Date, nullable=False)
    close_price = Column(Numeric, nullable=False)
    
    asset = relationship("Asset", back_populates="daily_returns")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)