from fastapi import FastAPI
from app.database import engine, Base
from app.routers import customers, rooms, bookings, auth

app = FastAPI(title="Smart Hotel Management System")

Base.metadata.create_all(bind=engine)

app.include_router(customers.router)
app.include_router(rooms.router)
app.include_router(bookings.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Smart Hotel Management System API is running"}