"""
train_pricing.py
-----------------
Dynamic Pricing model — REGRESSION.
Input: booking features (room type, lead_time, season, etc.)
Output: predicted price (in INR — base currency)

Run:  python -m app.ml.train_pricing
Output: app/ml/models/pricing_model.pkl
        app/ml/models/pricing_encoders.pkl
"""

import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, r2_score

BASE_DIR = os.path.dirname(__file__)
CSV_PATH = os.path.join(BASE_DIR, "hotel_bookings.csv")
MODEL_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODEL_DIR, exist_ok=True)

# Currency conversion rates (base = INR).
# Yeh sirf DISPLAY ke liye hai — model hamesha INR me predict karega,
# frontend/API layer isse convert karke dikhayega.
CURRENCY_RATES = {
    "INR": 1.0,
    "USD": 0.012,
    "GBP": 0.0095,
    "EUR": 0.011,
    "AED": 0.044,
}


def load_data():
    df = pd.read_csv(CSV_PATH)
    return df


def prepare_features(df):
    """
    ML models sirf NUMBERS samajhte hai, text nahi.
    'room_type' aur 'season' jaise text columns ko LabelEncoder se
    numbers me convert karte hai (e.g. Single=0, Double=1, Deluxe=2, Suite=3).

    IMPORTANT: encoder ko save karna zaroori hai — kyunki prediction
    time pe (naya booking aane par) hume EXACT wahi encoding use karni
    hogi, warna model confuse ho jayega.
    """
    df = df.copy()
    encoders = {}

    for col in ["room_type", "season"]:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        encoders[col] = le  # baad me predictor.py isse dubara use karega

    feature_cols = [
        "room_type", "lead_time", "length_of_stay",
        "num_guests", "is_weekend", "season",
        "previous_cancellations", "special_requests",
    ]
    X = df[feature_cols]
    y = df["price"]  # target: price (regression)

    return X, y, encoders, feature_cols


def train():
    df = load_data()
    X, y, encoders, feature_cols = prepare_features(df)

    # 80% data training ke liye, 20% testing ke liye (model ne kabhi nahi dekha)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Random Forest: bahut saare "decision trees" ka average.
    # n_estimators=200 -> 200 trees banayega, jyada trees = zyada stable prediction.
    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=12,
        random_state=42,
        n_jobs=-1,  # saare CPU cores use karo, training fast hogi
    )
    model.fit(X_train, y_train)

    # --- Evaluate: model kitna accurate hai test data pe ---
    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)   # average error (INR me)
    r2 = r2_score(y_test, preds)                # 1.0 = perfect, 0 = bekaar

    print("===== Pricing Model Evaluation =====")
    print(f"MAE  (avg error): ₹{mae:.2f}")
    print(f"R² Score        : {r2:.4f}  (1.0 = perfect fit)")

    # --- Feature importance: kaunsa feature price ko sabse zyada affect karta hai ---
    importances = pd.Series(model.feature_importances_, index=feature_cols)
    print("\n--- Feature Importance ---")
    print(importances.sort_values(ascending=False).round(3))

    # --- Save model + encoders + feature order ---
    joblib.dump(model, os.path.join(MODEL_DIR, "pricing_model.pkl"))
    joblib.dump(encoders, os.path.join(MODEL_DIR, "pricing_encoders.pkl"))
    joblib.dump(feature_cols, os.path.join(MODEL_DIR, "pricing_features.pkl"))

    print(f"\n[OK] Model saved -> {MODEL_DIR}/pricing_model.pkl")


def convert_currency(amount_inr: float, target_currency: str = "INR") -> float:
    """
    INR amount ko kisi bhi supported currency me convert karta hai.
    Yeh function predictor.py aur API layer dono use karenge.
    """
    rate = CURRENCY_RATES.get(target_currency.upper())
    if rate is None:
        raise ValueError(
            f"Unsupported currency '{target_currency}'. "
            f"Supported: {list(CURRENCY_RATES.keys())}"
        )
    return round(amount_inr * rate, 2)


if __name__ == "__main__":
    train()