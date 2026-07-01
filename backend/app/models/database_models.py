from sqlalchemy import Column, Integer, String, Float, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="customer")  # "customer" | "admin" | "staff"

    bookings = relationship("Booking", back_populates="customer")


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    room_number = Column(String, unique=True, nullable=False)
    room_type = Column(String, nullable=False)  # e.g. "Single", "Double", "Suite"
    base_price = Column(Float, nullable=False)
    is_available = Column(Boolean, default=True)

    bookings = relationship("Booking", back_populates="room")


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    room_id = Column(Integer, ForeignKey("rooms.id"))
    check_in = Column(Date, nullable=False)
    check_out = Column(Date, nullable=False)
    predicted_price = Column(Float)          # ML model yahan se fill karega
    cancellation_risk = Column(Float)        # ML model yahan se fill karega
    status = Column(String, default="confirmed")  # confirmed / cancelled / completed

    customer = relationship("Customer", back_populates="bookings")
    room = relationship("Room", back_populates="bookings")
