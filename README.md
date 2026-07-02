# 🏨 Smart Hotel Management System

A full-stack hotel management platform with **AI-powered dynamic pricing** and **cancellation risk prediction**, built with React, FastAPI, and scikit-learn.

**Live Demo:** [Frontend](#) · [API Docs](#) &nbsp;*(links added after deployment)*

![Tech Stack](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=white) ![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white) ![Python](https://img.shields.io/badge/Python-3.9-3776AB?logo=python&logoColor=white) ![scikit--learn](https://img.shields.io/badge/scikit--learn-F7931E?logo=scikitlearn&logoColor=white) ![SQLite](https://img.shields.io/badge/SQLite-07405E?logo=sqlite&logoColor=white)

---

## ✨ Features

- 🔐 **JWT Authentication** with role-based access control (Customer / Admin / Staff)
- 🏠 **Room Management** — full CRUD, admin-only write access
- 📅 **Booking System** — customers book rooms, admins manage all bookings
- 🤖 **AI Dynamic Pricing** — a Random Forest regression model predicts room price based on room type, season, stay length, lead time, and more
- ⚠️ **Cancellation Risk Prediction** — a Random Forest classifier estimates the probability a booking will be cancelled, giving hotels early warning
- 🎨 **Modern, responsive UI** — glassmorphism design with smooth animations
- 🛡️ **Protected routes** — customers and admins see different views and permissions

---

## 🧱 Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React (Vite), React Router, Tailwind CSS, Axios |
| Backend | FastAPI, SQLAlchemy, Pydantic |
| Database | SQLite (dev) |
| Auth | JWT (python-jose), bcrypt password hashing |
| Machine Learning | scikit-learn (RandomForestRegressor, RandomForestClassifier) |
| Deployment | Render (backend) · Vercel (frontend) |

---

## 🏗️ Architecture

```
┌─────────────────┐        HTTPS/JSON        ┌──────────────────┐
│  React Frontend  │ ────────────────────────▶│  FastAPI Backend  │
│  (Vite + Tailwind)│◀──────────────────────── │  (JWT protected)  │
└─────────────────┘                           └─────────┬────────┘
                                                          │
                                    ┌─────────────────────┼─────────────────────┐
                                    ▼                     ▼                     ▼
                              ┌───────────┐        ┌────────────┐       ┌──────────────┐
                              │  SQLite   │        │  ML Models  │       │  Auth Layer   │
                              │  (bookings,│        │  (pricing +│       │  (JWT + roles)│
                              │  rooms,    │        │ cancellation)│      │               │
                              │  customers)│        └────────────┘       └──────────────┘
                              └───────────┘
```

---

## 🤖 Machine Learning Details

Two models are trained on a synthetically generated but rule-based dataset (`app/ml/generate_dataset.py`) that encodes realistic pricing and cancellation patterns.

### 1. Dynamic Pricing (Regression)
- **Model:** RandomForestRegressor
- **Features:** room type, lead time, length of stay, guest count, weekend flag, season, prior cancellations, special requests
- **Performance:** R² ≈ 0.99, MAE ≈ ₹1,700
- **Key drivers:** length of stay and room type dominate price, followed by season

### 2. Cancellation Risk (Classification)
- **Model:** RandomForestClassifier (balanced class weights)
- **Output:** cancellation probability (0–1), not just a binary label
- **Key drivers:** lead time and prior cancellation history are the strongest predictors

Both models are trained offline (`train_pricing.py`, `train_cancellation.py`), saved as `.pkl` files, and loaded once at API startup via `app/ml/predictor.py` for fast inference on every booking.

---

## 📂 Project Structure

```
smart-hotel-system/
├── backend/
│   ├── app/
│   │   ├── auth/            # JWT security, dependencies, role guards
│   │   ├── ml/               # dataset generation, training scripts, predictor
│   │   ├── models/           # SQLAlchemy models
│   │   ├── routers/          # API routes (auth, customers, rooms, bookings)
│   │   ├── database.py
│   │   ├── main.py
│   │   └── schemas.py        # Pydantic schemas
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── api/               # Axios client + endpoint functions
    │   ├── components/        # Navbar, ProtectedRoute
    │   ├── context/           # AuthContext
    │   ├── pages/              # Home, Login, Register, Rooms, Bookings, AdminRooms
    │   └── App.jsx
    └── package.json
```

---

## 🚀 Running Locally

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Train the ML models (one-time)
python -m app.ml.generate_dataset
python -m app.ml.train_pricing
python -m app.ml.train_cancellation

uvicorn app.main:app --reload
```
API runs at `http://127.0.0.1:8000` · Interactive docs at `/docs`

### Frontend
```bash
cd frontend
npm install
npm run dev
```
App runs at `http://localhost:5173`

> Create a `.env` in `backend/` with `SECRET_KEY=<your-secret>` before running in any shared environment.

---

## 🔑 API Overview

| Endpoint | Method | Access |
|---|---|---|
| `/auth/register` | POST | Public |
| `/auth/login` | POST | Public |
| `/rooms/` | GET | Public |
| `/rooms/` | POST/PUT/DELETE | Admin/Staff |
| `/bookings/` | POST | Authenticated (customer) |
| `/bookings/` | GET | Authenticated (own bookings / all for admin) |
| `/bookings/{id}/status` | PUT | Admin/Staff |
| `/bookings/{id}` | DELETE | Admin/Staff |

Full interactive API reference available at `/docs` (Swagger UI).

---

## 🗺️ Roadmap / Possible Extensions
- [ ] Alembic migrations for schema versioning
- [ ] Date-overlap validation on bookings
- [ ] Automated tests (pytest)
- [ ] Payment gateway integration
- [ ] Email notifications on booking confirmation/cancellation

---

## 👩‍💻 Author

Built by [Tanishka Gupta](https://github.com/Tanishkag23)
