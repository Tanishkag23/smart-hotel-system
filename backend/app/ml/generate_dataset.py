"""
generate_dataset.py
--------------------
Real historical booking data humare paas nahi hai (naya system hai),
isliye hum SYNTHETIC data banate hai. Lekin fully random nahi —
har feature ka price/cancellation se ek logical rule hota hai,
taaki ML model asli patterns seekhe (na ki noise).

Run:  python -m app.ml.generate_dataset
Output: app/ml/hotel_bookings.csv
"""

import os
import numpy as np
import pandas as pd

# ---- Reproducibility ----
# seed fix karne se har baar SAME random data banega.
# Isse aapke aur mere results match karenge (debugging aasaan).
RNG = np.random.default_rng(seed=42)

# Kitne fake bookings banane hai
N_SAMPLES = 5000

# ---- Config: room types aur unka base price (INR me) ----
# Yeh base price se pricing model start karega, phir features add/subtract karenge.
ROOM_TYPES = {
    "Single":  1500,
    "Double":  2500,
    "Deluxe":  4000,
    "Suite":   7000,
}

SEASONS = ["low", "mid", "high"]
# Season ka price pe multiplier — high season me daam badhte hai (dynamic pricing).
SEASON_MULTIPLIER = {"low": 0.85, "mid": 1.0, "high": 1.35}


def generate():
    n = N_SAMPLES

    # --- Step A: raw features randomly generate karo ---
    room_type = RNG.choice(list(ROOM_TYPES.keys()), size=n)

    # lead_time: booking aur check-in ke beech ke din (0 se 120)
    # Zyada realistic distribution: zyadatar log 1-30 din pehle book karte hai.
    lead_time = RNG.integers(0, 121, size=n)

    # length_of_stay: kitni raatein (1 se 14)
    length_of_stay = RNG.integers(1, 15, size=n)

    # num_guests: 1 se 4
    num_guests = RNG.integers(1, 5, size=n)

    # is_weekend: 0 ya 1
    is_weekend = RNG.integers(0, 2, size=n)

    season = RNG.choice(SEASONS, size=n, p=[0.4, 0.35, 0.25])

    # previous_cancellations: customer ne pehle kitni baar cancel kiya (0-5)
    # Zyadatar log 0, kuch log repeat-canceller.
    previous_cancellations = RNG.choice(
        [0, 1, 2, 3, 4, 5], size=n, p=[0.6, 0.2, 0.1, 0.05, 0.03, 0.02]
    )

    # special_requests: 0-5 (extra pillow, late checkout, etc.)
    special_requests = RNG.integers(0, 6, size=n)

    df = pd.DataFrame({
        "room_type": room_type,
        "lead_time": lead_time,
        "length_of_stay": length_of_stay,
        "num_guests": num_guests,
        "is_weekend": is_weekend,
        "season": season,
        "previous_cancellations": previous_cancellations,
        "special_requests": special_requests,
    })

    # --- Step B: PRICE banao (yeh regression ka target hai) ---
    # base price room type se
    base = df["room_type"].map(ROOM_TYPES).astype(float)

    # season multiplier
    season_mult = df["season"].map(SEASON_MULTIPLIER)

    price = base * season_mult

    # weekend pe +15%
    price *= np.where(df["is_weekend"] == 1, 1.15, 1.0)

    # har extra guest pe +8%
    price *= (1 + 0.08 * (df["num_guests"] - 1))

    # lambe stay pe halka discount (per night sasta): -1% per night after 1st
    price *= (1 - 0.01 * (df["length_of_stay"] - 1))

    # last-minute (kam lead_time) pe thoda premium — urgency pricing
    price *= np.where(df["lead_time"] < 3, 1.10, 1.0)

    # thoda realistic noise daalo (±5%) taaki model perfect na ho jaye
    price *= RNG.normal(1.0, 0.05, size=n)

    # per-night price ko total stay se multiply — final bill
    price = price * df["length_of_stay"]

    df["price"] = price.round(0)  # INR me round figure

    # --- Step C: CANCELLATION banao (yeh classification ka target hai) ---
    # Hum ek "risk score" banate hai rules se, phir usse probability me badalte hai.
    risk = np.zeros(n)

    # lambe lead time = zyada risk (log plan change kar lete hai)
    risk += df["lead_time"] * 0.015

    # pehle cancel kiya hai to bahut zyada risk (strongest signal)
    risk += df["previous_cancellations"] * 0.6

    # zyada special requests = committed guest = KAM risk (isliye minus)
    risk -= df["special_requests"] * 0.15

    # weekend bookings thodi zyada stable
    risk -= df["is_weekend"] * 0.1

    # sigmoid se risk ko 0-1 probability me convert karo
    prob_cancel = 1 / (1 + np.exp(-(risk - 1.2)))

    # probability ke hisaab se 0/1 draw karo
    df["is_cancelled"] = (RNG.random(n) < prob_cancel).astype(int)

    return df


if __name__ == "__main__":
    df = generate()

    # file isi ml/ folder ke andar save karo
    out_path = os.path.join(os.path.dirname(__file__), "hotel_bookings.csv")
    df.to_csv(out_path, index=False)

    print(f"[OK] {len(df)} rows generate hue -> {out_path}")
    print("\n--- Sample ---")
    print(df.head())
    print("\n--- Cancellation balance (0=stayed, 1=cancelled) ---")
    print(df["is_cancelled"].value_counts(normalize=True).round(3))
    print("\n--- Price stats (INR) ---")
    print(df["price"].describe().round(0))
