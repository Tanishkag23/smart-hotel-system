from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.database_models import Booking, Customer, Room
from app.schemas import BookingCreate, BookingResponse
from app.ml.predictor import predict_booking
from app.auth.dependencies import get_current_user, require_role

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)

# CREATE - nayi booking banana (logged-in customer ke naam pe)
@router.post("/", response_model=BookingResponse)
def create_booking(
    booking: BookingCreate,
    db: Session = Depends(get_db),
    current_user: Customer = Depends(get_current_user),
):
    room = db.query(Room).filter(Room.id == booking.room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    ml_result = predict_booking(
        room_type=room.room_type,
        check_in=booking.check_in,
        check_out=booking.check_out,
        num_guests=getattr(booking, "num_guests", 1),
    )

    db_booking = Booking(
        customer_id=current_user.id,   # ab token se aayega, body se nahi
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


# READ ALL - admin/staff sabki bookings dekh sakte hai, customer sirf apni
@router.get("/", response_model=list[BookingResponse])
def get_bookings(
    db: Session = Depends(get_db),
    current_user: Customer = Depends(get_current_user),
):
    if current_user.role in ("admin", "staff"):
        return db.query(Booking).all()
    return db.query(Booking).filter(Booking.customer_id == current_user.id).all()


# READ ONE
@router.get("/{booking_id}", response_model=BookingResponse)
def get_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: Customer = Depends(get_current_user),
):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if current_user.role not in ("admin", "staff") and booking.customer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed to view this booking")
    return booking


# UPDATE - status change karna: sirf admin/staff
@router.put("/{booking_id}/status")
def update_booking_status(
    booking_id: int,
    new_status: str,
    db: Session = Depends(get_db),
    current_user: Customer = Depends(require_role("admin", "staff")),
):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    booking.status = new_status
    db.commit()
    db.refresh(booking)
    return booking


# DELETE - sirf admin/staff
@router.delete("/{booking_id}")
def delete_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: Customer = Depends(require_role("admin", "staff")),
):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    db.delete(booking)
    db.commit()
    return {"message": "Booking deleted successfully"}
