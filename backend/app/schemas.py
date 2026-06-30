from pydantic import BaseModel
from datetime import date
from typing import Optional

class CustomerCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None

class CustomerResponse(CustomerCreate):
    id: int

    class Config:
        from_attributes = True


class RoomCreate(BaseModel):
    room_number: str
    room_type: str
    base_price: float

class RoomResponse(RoomCreate):
    id: int
    is_available: bool

    class Config:
        from_attributes = True


class BookingCreate(BaseModel):
    customer_id: int
    room_id: int
    check_in: date
    check_out: date

class BookingResponse(BookingCreate):
    id: int
    predicted_price: Optional[float] = None
    cancellation_risk: Optional[float] = None
    status: str

    class Config:
        from_attributes = True