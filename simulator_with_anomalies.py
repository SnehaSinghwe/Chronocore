"""
simulator_with_anomalies.py
----------------------------
Generates a labeled dataset of 500 readings (300 normal, 200 anomalous)
for training and evaluating IsolationForest.

Anomaly types injected:
  1. fan_failure   — Fan 2 drops to 0 while temp is high
  2. overheat      — Temperature spikes above 34°C
  3. underspeed    — Both fans slow to < 50 RPM
  4. combined      — Fan failure + overheat simultaneously
"""

import os
import json
import random
import numpy as np
from datetime import datetime, timedelta

random.seed(42)
np.random.seed(42)

os.makedirs("data", exist_ok=True)

# ── helpers ──────────────────────────────────────────────────────────────────

def _ts(base: datetime, i: int) -> str:
    return (base + timedelta(seconds=5 * i)).strftime("%Y-%m-%d %H:%M:%S")


def normal_reading(base, i):
    return {
        "timestamp":   _ts(base, i),
        "fan_1_speed": random.randint(75, 90),
        "fan_2_speed": random.randint(60, 85),
        "temperature": round(random.uniform(22.0, 28.0), 2),
        "label":       0,          # 0 = normal
        "anomaly_type": "none",
    }


def anomaly_reading(base, i, kind=None):
    if kind is None:
        kind = random.choice(["fan_failure", "overheat", "underspeed", "combined"])

    if kind == "fan_failure":
        return {
            "timestamp":   _ts(base, i),
            "fan_1_speed": random.randint(75, 90),
            "fan_2_speed": 0,                            # fan dead
            "temperature": round(random.uniform(28.5, 33.0), 2),  # temp rises
            "label":       1,
            "anomaly_type": kind,
        }
    elif kind == "overheat":
        return {
            "timestamp":   _ts(base, i),
            "fan_1_speed": random.randint(70, 90),
            "fan_2_speed": random.randint(60, 85),
            "temperature": round(random.uniform(34.0, 42.0), 2),  # spike
            "label":       1,
            "anomaly_type": kind,
        }
    elif kind == "underspeed":
        return {
            "timestamp":   _ts(base, i),
            "fan_1_speed": random.randint(20, 48),
            "fan_2_speed": random.randint(20, 48),
            "temperature": round(random.uniform(22.0, 28.0), 2),
            "label":       1,
            "anomaly_type": kind,
        }
    else:  # combined
        return {
            "timestamp":   _ts(base, i),
            "fan_1_speed": random.randint(75, 90),
            "fan_2_speed": 0,
            "temperature": round(random.uniform(34.0, 42.0), 2),
            "label":       1,
            "anomaly_type": kind,
        }


# ── generate dataset ──────────────────────────────────────────────────────────

N_NORMAL    = 300
N_ANOMALOUS = 200
base_time   = datetime(2024, 1, 1, 8, 0, 0)

normal_data   = [normal_reading(base_time, i)            for i in range(N_NORMAL)]
anomaly_kinds = ["fan_failure", "overheat", "underspeed", "combined"]
anomaly_data  = [
    anomaly_reading(base_time, N_NORMAL + i, kind=anomaly_kinds[i % 4])
    for i in range(N_ANOMALOUS)
]

dataset = normal_data + anomaly_data
random.shuffle(dataset)

out_path = "data/labeled_dataset.json"
with open(out_path, "w") as f:
    json.dump(dataset, f, indent=2)

print(f"✅  Dataset saved → {out_path}")
print(f"   Normal readings   : {N_NORMAL}")
print(f"   Anomalous readings: {N_ANOMALOUS}")
print(f"   Total             : {len(dataset)}")
