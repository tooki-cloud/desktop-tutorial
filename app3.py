#モデルを機械学習させて戻り値を得る
import pandas as pd
import os
import time
from sklearn.ensemble import RandomForestClassifier

def run_prediction_loop():
    # 訓練データ読み込み・モデル学習
    X_train = pd.read_csv("X_future_deviation.csv")
    y_train = pd.read_csv("y_future_deviation.csv").values.ravel()

    model = RandomForestClassifier(n_estimators=100, max_depth=3, random_state=42)
    model.fit(X_train, y_train)

    # 監視対象ファイル
    CSV_FILE = "データ.csv"

    while True:
        if os.path.exists(CSV_FILE):
            df = pd.read_csv(CSV_FILE, sep="|", encoding="utf-8")
            df.columns = ["時刻", "規格値", "pH", "溶出時間", "作業員ID", "温度", "湿度", "ロット番号"]

            # 最低限のデータ数があるか（例：5点以上）
            if len(df) >= 5:
                latest_row = df.tail(1).drop(columns=["時刻"])

                # 特徴量整形（カテゴリ変数のダミー変換）
                latest_encoded = pd.get_dummies(latest_row, columns=["作業員ID", "ロット番号"])
                X_input = latest_encoded.reindex(columns=X_train.columns, fill_value=0)

                # 逸脱確率予測
                prob = model.predict_proba(X_input)[0][1]
                print(f" [予測] この状態で10行以内に逸脱する確率: {prob:.4f}")

                with open("latest_prob.json", "w", encoding="utf-8") as f:
                    f.write(f'{{"prob": {prob:.4f}}}')
        
        time.sleep(1)  