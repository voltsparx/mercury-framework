"""Simulated sensors - provide fake sensor readings (accelerometer, GPS).

Harmless data for UI demos and compatibility testing.
"""
import random
from typing import Dict


def sensor_readings() -> Dict[str, float]:
    return {
        "accelerometer_x": round(random.uniform(-1.0, 1.0), 3),
        "accelerometer_y": round(random.uniform(-1.0, 1.0), 3),
        "accelerometer_z": round(random.uniform(-1.0, 1.0), 3),
        "gps_lat": round(random.uniform(-90.0, 90.0), 6),
        "gps_lon": round(random.uniform(-180.0, 180.0), 6),
    }


if __name__ == "__main__":
    print(sensor_readings())
