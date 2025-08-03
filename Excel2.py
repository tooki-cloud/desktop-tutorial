import time
import pandas as pd
import os
import random
from datetime import datetime

def run_prediction_loop():
    FILE_NAME = "データ.csv"
    MAX_ROWS = 1000

    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, mode="w", encoding="utf-8", newline="") as f:
            f.write("時刻|規格値|pH|溶出時間|作業員ID|温度|湿度|ロット番号\n")

    with open(FILE_NAME, mode="r", encoding="utf-8") as f:
        current_rows = sum(1 for _ in f) - 1

    while current_rows < MAX_ROWS:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        value = round(49.50 + random.uniform(-0.2, 0.2), 2)      # 規格値（平均49.5）
        pH = round(6.80 + random.uniform(-0.05, 0.05), 2)        # pH（微小変動）
        time_ = round(82.0 + random.uniform(-0.3, 0.3), 2)       # 溶出時間
        worker = random.choice(["A01", "B02", "C03"])
        temp = round(25.0 + random.uniform(-0.2, 0.2), 2)        # 温度
        humid = round(60.0 + random.uniform(-1, 1), 2)           # 湿度
        lot = f"LT{random.randint(1000, 9999)}"

        with open(FILE_NAME, mode="a", encoding="utf-8", newline="") as f:
            f.write(f"{now}|{value}|{pH}|{time_}|{worker}|{temp}|{humid}|{lot}\n")

        current_rows += 1
        time.sleep(1)