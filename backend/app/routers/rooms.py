from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.database_models import Room, Customer
from app.schemas import RoomCreate, RoomResponse
from app.auth.dependencies import require_role

router = APIRouter(
    prefix="/rooms",
    tags=["Rooms"]
)

# CREATE - naya room add karna (sirf admin/staff)
@router.post("/", response_model=RoomResponse)
def create_room(
    room: RoomCreate,
    db: Session = Depends(get_db),
    current_user: Customer = Depends(require_role("admin", "staff")),
):
    db_room = Room(**room.dict())
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room


# READ ALL - saare rooms ki list (public, sabko dikhna chahiye)
@router.get("/", response_model=list[RoomResponse])
def get_rooms(db: Session = Depends(get_db)):
    return db.query(Room).all()


# READ ONE - ek specific room (ID se) (public)
@router.get("/{room_id}", response_model=RoomResponse)
def get_room(room_id: int, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room


# UPDATE - room details change karna (sirf admin/staff)
@router.put("/{room_id}", response_model=RoomResponse)
def update_room(
    room_id: int,
    updated_data: RoomCreate,
    db: Session = Depends(get_db),
    current_user: Customer = Depends(require_role("admin", "staff")),
):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    room.room_number = updated_data.room_number
    room.room_type = updated_data.room_type
    room.base_price = updated_data.base_price

    db.commit()
    db.refresh(room)
    return room


# DELETE - room remove karna (sirf admin/staff)
@router.delete("/{room_id}")
def delete_room(
    room_id: int,
    db: Session = Depends(get_db),
    current_user: Customer = Depends(require_role("admin", "staff")),
):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    db.delete(room)
    db.commit()
    return {"message": "Room deleted successfully"}