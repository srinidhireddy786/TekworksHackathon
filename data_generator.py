import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)

routes = [
    ("Hyderabad", "Vijayawada"),
    ("Hyderabad", "Bangalore"),
    ("Chennai", "Coimbatore"),
    ("Delhi", "Agra"),
    ("Mumbai", "Pune")
]

data = []

start_date = datetime(2026, 1, 1)

for i in range(180):  # 6 months data
    date = start_date + timedelta(days=i)
    is_weekend = 1 if date.weekday() >= 5 else 0
    is_holiday = 1 if random.random() < 0.1 else 0

    for route in routes:
        base_passengers = random.randint(200, 500)

        # Increase demand on weekends/holidays
        if is_weekend:
            base_passengers += random.randint(50, 150)
        if is_holiday:
            base_passengers += random.randint(100, 200)

        seat_capacity = 600
        coaches = random.randint(10, 15)
        platform = random.randint(1, 6)
        delay = random.randint(0, 60)

        data.append([
            f"T{random.randint(100,999)}",
            route[0],
            route[1],
            date,
            base_passengers,
            seat_capacity,
            coaches,
            platform,
            delay,
            is_weekend,
            is_holiday
        ])

columns = [
    "Train_ID",
    "Source",
    "Destination",
    "Date",
    "Passenger_Count",
    "Seat_Capacity",
    "Coaches",
    "Platform",
    "Delay_Min",
    "Is_Weekend",
    "Is_Holiday"
]

df = pd.DataFrame(data, columns=columns)
df.to_csv("railway_data.csv", index=False)

print("Dataset Generated Successfully!")