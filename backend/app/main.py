from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import customers, rooms, bookings, auth

app = FastAPI(title="Smart Hotel Management System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # frontend ka URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(customers.router)
app.include_router(rooms.router)
app.include_router(bookings.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Smart Hotel Management System API is running"}