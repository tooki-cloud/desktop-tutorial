import os
import pandas as pd
import datetime
import time
import random
import threading
from app3 import run_prediction_loop

FILE_NAME = "データ.csv"
MAX_ROWS = 1000

prediction_thread = threading.Thread(target=run_prediction_loop, daemon=True)
prediction_thread.start()

# 初期ヘッダー書き込み
if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, mode="w", encoding="utf-8", newline="") as f:
        f.write("時刻|規格値|pH|溶出時間|作業員ID|温度|湿度|ロット番号\n")

# 既存行数の確認
with open(FILE_NAME, mode="r", encoding="utf-8") as f:
    current_rows = sum(1 for _ in f) - 1

# データ生成ループ
while current_rows < MAX_ROWS:
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    value = round(50 + 5 * (0.5 - time.time() % 1), 2)
    pH = round(6.8 + 0.5 * (0.5 - time.time() % 1) + random.uniform(-0.1, 0.1), 2)
    dissolution = round(85 + 15 * (0.5 - time.time() % 1) + random.uniform(-1, 1), 2)

    # 追加項目
    worker_id = random.choice(["W001", "W002", "W003", "W004", "W005"])
    temperature = round(random.uniform(22.0, 27.0), 1)
    humidity = random.randint(40, 60)
    lot_number = "LOT" + datetime.datetime.now().strftime("%Y%m%d") + str(random.randint(1000, 9999))

    # 書き込み
    with open(FILE_NAME, mode="a", encoding="utf-8", newline="") as f:
        f.write(f"{now}|{value}|{pH}|{dissolution}|{worker_id}|{temperature}|{humidity}|{lot_number}\n")

    current_rows += 1
    time.sleep(1)

