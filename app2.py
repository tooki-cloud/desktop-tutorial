#trainデータを作成する
import pandas as pd
import pandas as pd

CSV_FILE = "データ.csv"
GROUP_SIZE = 5
df = pd.read_csv(CSV_FILE, sep="|", encoding="utf-8")
df.columns = ["時刻", "規格値", "pH", "溶出時間", "作業員ID", "温度", "湿度", "ロット番号"]
df = df.reset_index(drop=True)

# ---------- 全体の統計量 ----------
spec_mean = df["規格値"].mean()
spec_std = df["規格値"].std()
UCL = spec_mean +  spec_std
LCL = spec_mean -  spec_std

print(f"規格値のUCL: {UCL:.2f}, LCL: {LCL:.2f}")

X_raw = []
y = []

# ---------- データ分割・ラベル作成 ----------
for i in range(len(df) - 10):
    row = df.iloc[i].copy()
    row.pop("時刻")  # 時刻は除外
    X_raw.append(row)

    future = df.iloc[i+1:i+11].reset_index(drop=True)
    deviation_found = False

    # 5点1群ごとに逸脱チェック
    for j in range(len(future) - GROUP_SIZE + 1):
        group = future.iloc[j:j+GROUP_SIZE]
        group_mean = group["規格値"].mean()
        if group_mean > UCL or group_mean < LCL:
            deviation_found = True
            break

    y.append(int(deviation_found))

# ---------- 特徴量変換 ----------
X_df = pd.DataFrame(X_raw)
X_encoded = pd.get_dummies(X_df, columns=["作業員ID", "ロット番号"])
X_encoded = X_encoded.astype(int)
X_encoded.to_csv("X_future_deviation.csv", index=False)
pd.Series(y).to_csv("y_future_deviation.csv", index=False)

print("✅ 統計的逸脱定義に基づき、学習データを作成しました")