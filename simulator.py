"""Streams fake IoT sensor readings into a Tiger Data hypertable.

Usage: TIGER_URL="postgres://..." python simulator.py
"""
import math
import os
import random
import time

import psycopg2

SENSORS = ["sensor-a", "sensor-b", "sensor-c", "sensor-d"]


def main():
    conn = psycopg2.connect(os.environ["TIGER_URL"])
    conn.autocommit = True
    cur = conn.cursor()
    with open(os.path.join(os.path.dirname(__file__), "schema.sql")) as f:
        cur.execute(f.read())

    print("Streaming events. Ctrl+C to stop.")
    n = 0
    while True:
        t = time.time()
        for i, s in enumerate(SENSORS):
            temp = 22 + 4 * math.sin(t / 30 + i) + random.gauss(0, 0.4)
            if random.random() < 0.02:  # occasional spike to trigger alerts
                temp += 10
            hum = 50 + 10 * math.cos(t / 40 + i) + random.gauss(0, 1)
            cur.execute(
                "INSERT INTO sensor_events (time, sensor_id, temperature, humidity)"
                " VALUES (now(), %s, %s, %s)",
                (s, round(temp, 2), round(hum, 2)),
            )
            n += 1
        if n % 40 == 0:
            print(f"{n} events inserted")
        time.sleep(1)


if __name__ == "__main__":
    main()
