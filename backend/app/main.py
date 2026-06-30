from fastapi import FastAPI
from app.database import engine, Base

app = FastAPI(title="Smart Hotel Management System")

# Yeh line database tables create kar degi agar already nahi bani
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Smart Hotel Management System API is running"}