from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.database_models import Booking, Customer, Room
from app.schemas import BookingCreate, BookingResponse
from app.ml.predictor import predict_booking

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)

# CREATE - nayi booking banana
@router.post("/", response_model=BookingResponse)
def create_booking(booking: BookingCreate, db: Session = Depends(get_db)):
    # Pehle check karo customer exist karta hai
    customer = db.query(Customer).filter(Customer.id == booking.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Phir check karo room exist karta hai
    room = db.query(Room).filter(Room.id == booking.room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    # ML models se price aur cancellation risk predict karo
    ml_result = predict_booking(
        room_type=room.room_type,
        check_in=booking.check_in,
        check_out=booking.check_out,
        num_guests=getattr(booking, "num_guests", 1),
    )

    db_booking = Booking(
        customer_id=booking.customer_id,
        room_id=booking.room_id,
        check_in=booking.check_in,
        check_out=booking.check_out,
        predicted_price=ml_result["predicted_price_inr"],
        cancellation_risk=ml_result["cancellation_risk"],
        status="confirmed"
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking


# READ ALL - saari bookings ki list
@router.get("/", response_model=list[BookingResponse])
def get_bookings(db: Session = Depends(get_db)):
    return db.query(Booking).all()


# READ ONE - ek specific booking
@router.get("/{booking_id}", response_model=BookingResponse)
def get_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


# UPDATE - booking status change karna (jaise "cancelled" mark karna)
@router.put("/{booking_id}/status")
def update_booking_status(booking_id: int, new_status: str, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    booking.status = new_status
    db.commit()
    db.refresh(booking)
    return booking


# DELETE - booking cancel/remove karna
@router.delete("/{booking_id}")
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    db.delete(booking)
    db.commit()
    return {"message": "Booking deleted successfully"}