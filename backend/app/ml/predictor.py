"""
predictor.py
------------
Loads trained models and exposes functions to predict:
- price (with currency conversion)
- cancellation_risk (probability 0-1)

Usage (from FastAPI routes):
    from app.ml.predictor import predict_booking

    result = predict_booking(
        room_type="Deluxe",
        check_in="2026-08-10",
        check_out="2026-08-13",
        num_guests=2,
        special_requests=1,
        previous_cancellations=0,
        booking_date="2026-07-02",   # optional, defaults to today
        currency="USD",              # optional, defaults to INR
    )
    # result = {
    #   "predicted_price_inr": 8450.0,
    #   "predicted_price": 101.4,
    #   "currency": "USD",
    #   "cancellation_risk": 0.23
    # }
"""

import os
from datetime import date, datetime
import joblib
import pandas as pd

BASE_DIR = os.path.dirname(__file__)
MODEL_DIR = os.path.join(BASE_DIR, "models")

CURRENCY_RATES = {
    "INR": 1.0,
    "USD": 0.012,
    "GBP": 0.0095,
    "EUR": 0.011,
    "AED": 0.044,
}

# ---- Load models once at import time (not on every request) ----
_pricing_model = joblib.load(os.path.join(MODEL_DIR, "pricing_model.pkl"))
_pricing_encoders = joblib.load(os.path.join(MODEL_DIR, "pricing_encoders.pkl"))
_pricing_features = joblib.load(os.path.join(MODEL_DIR, "pricing_features.pkl"))

_cancel_model = joblib.load(os.path.join(MODEL_DIR, "cancellation_model.pkl"))
_cancel_encoders = joblib.load(os.path.join(MODEL_DIR, "cancellation_encoders.pkl"))
_cancel_features = joblib.load(os.path.join(MODEL_DIR, "cancellation_features.pkl"))


def _parse_date(d):
    if isinstance(d, (date, datetime)):
        return d if isinstance(d, date) and not isinstance(d, datetime) else d.date()
    return datetime.strptime(d, "%Y-%m-%d").date()


def _encode_value(encoder, value, fallback_index=0):
    """Safely encode a category; falls back if unseen label given."""
    classes = list(encoder.classes_)
    if value not in classes:
        value = classes[fallback_index]
    return encoder.transform([value])[0]


def convert_currency(amount_inr: float, target_currency: str = "INR") -> float:
    rate = CURRENCY_RATES.get(target_currency.upper())
    if rate is None:
        raise ValueError(
            f"Unsupported currency '{target_currency}'. "
            f"Supported: {list(CURRENCY_RATES.keys())}"
        )
    return round(amount_inr * rate, 2)


def _build_feature_row(
    room_type,
    check_in,
    check_out,
    num_guests,
    special_requests,
    previous_cancellations,
    booking_date,
    encoders,
    feature_cols,
):
    check_in = _parse_date(check_in)
    check_out = _parse_date(check_out)
    booking_date = _parse_date(booking_date) if booking_date else date.today()

    lead_time = max((check_in - booking_date).days, 0)
    length_of_stay = max((check_out - check_in).days, 1)
    is_weekend = int(check_in.weekday() in (4, 5))  # Fri/Sat as weekend flag

    # season: simple month-based rule (India context)
    month = check_in.month
    if month in (12, 1, 2, 10, 11):
        season = "high"
    elif month in (6, 7, 8, 9):
        season = "low"
    else:
        season = "mid"

    row = {
        "room_type": _encode_value(encoders["room_type"], room_type),
        "lead_time": lead_time,
        "length_of_stay": length_of_stay,
        "num_guests": num_guests,
        "is_weekend": is_weekend,
        "season": _encode_value(encoders["season"], season),
        "previous_cancellations": previous_cancellations,
        "special_requests": special_requests,
    }
    return pd.DataFrame([row])[feature_cols]


def predict_price(
    room_type,
    check_in,
    check_out,
    num_guests=1,
    special_requests=0,
    previous_cancellations=0,
    booking_date=None,
    currency="INR",
):
    X = _build_feature_row(
        room_type, check_in, check_out, num_guests,
        special_requests, previous_cancellations, booking_date,
        _pricing_encoders, _pricing_features,
    )
    price_inr = float(_pricing_model.predict(X)[0])
    price_inr = round(price_inr, 2)
    return {
        "predicted_price_inr": price_inr,
        "predicted_price": convert_currency(price_inr, currency),
        "currency": currency.upper(),
    }


def predict_cancellation_risk(
    room_type,
    check_in,
    check_out,
    num_guests=1,
    special_requests=0,
    previous_cancellations=0,
    booking_date=None,
):
    X = _build_feature_row(
        room_type, check_in, check_out, num_guests,
        special_requests, previous_cancellations, booking_date,
        _cancel_encoders, _cancel_features,
    )
    risk = float(_cancel_model.predict_proba(X)[0][1])  # probability of class "1"
    return round(risk, 4)


def predict_booking(
    room_type,
    check_in,
    check_out,
    num_guests=1,
    special_requests=0,
    previous_cancellations=0,
    booking_date=None,
    currency="INR",
):
    """Convenience function: returns both price and cancellation risk together."""
    price_result = predict_price(
        room_type, check_in, check_out, num_guests,
        special_requests, previous_cancellations, booking_date, currency,
    )
    risk = predict_cancellation_risk(
        room_type, check_in, check_out, num_guests,
        special_requests, previous_cancellations, booking_date,
    )
    return {**price_result, "cancellation_risk": risk}


if __name__ == "__main__":
    # Quick manual test
    result = predict_booking(
        room_type="Deluxe",
        check_in="2026-08-10",
        check_out="2026-08-13",
        num_guests=2,
        special_requests=1,
        previous_cancellations=0,
        currency="USD",
    )
    print(result)