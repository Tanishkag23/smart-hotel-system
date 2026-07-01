"""
train_cancellation.py
----------------------
Cancellation Prediction model — CLASSIFICATION.
Input: booking features (same as pricing model)
Output: is_cancelled (0 = will stay, 1 = will cancel) + probability

Run:  python -m app.ml.train_cancellation
Output: app/ml/models/cancellation_model.pkl
        app/ml/models/cancellation_encoders.pkl
"""

import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)

BASE_DIR = os.path.dirname(__file__)
CSV_PATH = os.path.join(BASE_DIR, "hotel_bookings.csv")
MODEL_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODEL_DIR, exist_ok=True)


def load_data():
    return pd.read_csv(CSV_PATH)


def prepare_features(df):
    """
    Pricing model ki tarah hi text columns ko encode karte hai.
    NOTE: yeh encoder pricing_encoders.pkl se ALAG file me save hoga.
    Dono models independent hai, isliye apna-apna encoder rakhna safe hai
    (agar kal ek model change karna pade to dusra affect nahi hoga).
    """
    df = df.copy()
    encoders = {}

    for col in ["room_type", "season"]:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        encoders[col] = le

    feature_cols = [
        "room_type", "lead_time", "length_of_stay",
        "num_guests", "is_weekend", "season",
        "previous_cancellations", "special_requests",
    ]
    X = df[feature_cols]
    y = df["is_cancelled"]  # target: 0 or 1 (classification)

    return X, y, encoders, feature_cols


def train():
    df = load_data()
    X, y, encoders, feature_cols = prepare_features(df)

    # stratify=y IMPORTANT hai: isse train aur test dono set me
    # 0 aur 1 ka RATIO same rahega (jaise dataset me hai).
    # Warna by chance test set me sirf ek hi class aa sakti hai.
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # class_weight="balanced": agar dataset thoda imbalanced ho
    # (jaise 60-40), to model minority class ko ignore na kare.
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        random_state=42,
        n_jobs=-1,
        class_weight="balanced",
    )
    model.fit(X_train, y_train)

    # --- Evaluate ---
    preds = model.predict(X_test)

    acc = accuracy_score(y_test, preds)
    prec = precision_score(y_test, preds)
    rec = recall_score(y_test, preds)
    f1 = f1_score(y_test, preds)
    cm = confusion_matrix(y_test, preds)

    print("===== Cancellation Model Evaluation =====")
    print(f"Accuracy  : {acc:.4f}")
    print(f"Precision : {prec:.4f}  (jab 'cancel' bola, kitni baar sahi tha)")
    print(f"Recall    : {rec:.4f}  (actual cancellations me se kitne pakde)")
    print(f"F1 Score  : {f1:.4f}  (precision aur recall ka balance)")

    print("\n--- Confusion Matrix ---")
    print("                Predicted: Stay   Predicted: Cancel")
    print(f"Actual: Stay        {cm[0][0]:>6}              {cm[0][1]:>6}")
    print(f"Actual: Cancel      {cm[1][0]:>6}              {cm[1][1]:>6}")
    print("\n(top-right + bottom-left = galat predictions, baaki sahi)")

    print("\n--- Detailed Report ---")
    print(classification_report(y_test, preds, target_names=["Stay", "Cancel"]))

    # --- Feature importance ---
    importances = pd.Series(model.feature_importances_, index=feature_cols)
    print("--- Feature Importance ---")
    print(importances.sort_values(ascending=False).round(3))

    # --- Save model + encoders + feature order ---
    joblib.dump(model, os.path.join(MODEL_DIR, "cancellation_model.pkl"))
    joblib.dump(encoders, os.path.join(MODEL_DIR, "cancellation_encoders.pkl"))
    joblib.dump(feature_cols, os.path.join(MODEL_DIR, "cancellation_features.pkl"))

    print(f"\n[OK] Model saved -> {MODEL_DIR}/cancellation_model.pkl")


if __name__ == "__main__":
    train()