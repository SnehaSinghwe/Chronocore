import os
import json
import random
import time
from datetime import datetime

# Create data directory if it doesn't exist
os.makedirs("data", exist_ok=True)

# Keep a list of last 20 readings (like a memory)
history = []

while True:
    # Generate simulated values
    fan_1_speed = random.randint(75, 90)  # Fan 1 usually running
    fan_2_speed = random.choice([0, random.randint(60, 85)])  # Fan 2 may fail
    temperature = round(random.uniform(24.0, 32.0), 2)  # Temperature in °C
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Create current reading
    data = {
        "timestamp": timestamp,
        "fan_1_speed": fan_1_speed,
        "fan_2_speed": fan_2_speed,
        "temperature": temperature
    }

    # Add to history
    history.append(data)

    # Keep only last 20 entries (rolling window)
    history = history[-20:]

    # Write current live reading
    with open("data/history.json", "w") as f:
        json.dump(data, f, indent=2)

    # Write full history for charting
    with open("data/history.json", "w") as f:
        json.dump(history, f, indent=2)

    print(f"[{timestamp}] Data written: Fan1={fan_1_speed}, Fan2={fan_2_speed}, Temp={temperature}°C")
    
    time.sleep(5)  # Wait 5 seconds before next reading
