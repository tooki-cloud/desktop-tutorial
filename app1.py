#C:\Users\tokok\anaconda3\python.exe -m streamlit run app1.py
#streamlitでwebアプリを作成する
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.family'] = 'MS Gothic' 
import time
import os
import json
import streamlit.components.v1 as components
import threading
import random
from datetime import datetime
import threading

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

        # 📌 変動幅を拡大（逸脱しやすく）
        value = round(49.50 + random.uniform(-0.4, 0.4), 2)       # 規格値（平均49.5 ±0.4）
        pH = round(6.80 + random.uniform(-0.10, 0.10), 2)          # pH（±0.10）
        time_ = round(82.0 + random.uniform(-0.6, 0.6), 2)         # 溶出時間（±0.6）

        worker = random.choice(["A01", "B02", "C03"])
        temp = round(25.0 + random.uniform(-0.5, 0.5), 2)          # 温度（±0.5）
        humid = round(60.0 + random.uniform(-2, 2), 2)             # 湿度（±2）
        lot = f"LT{random.randint(1000, 9999)}"

        with open(FILE_NAME, mode="a", encoding="utf-8", newline="") as f:
            f.write(f"{now}|{value}|{pH}|{time_}|{worker}|{temp}|{humid}|{lot}\n")

        current_rows += 1
        time.sleep(1)

        
st.markdown("""
    <style>
    .section-header {
        background-color: #1abc9c;
        color: white;
        padding: 0.5rem 1rem;
        font-weight: bold;
        font-size: 1.2rem;
        margin-top: 2rem;
        border-radius: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background-color: #2c3e50;
        color: white;
    }
    .sidebar-content {
        padding: 1rem;
    }
    .sidebar-content h2 {
        color: #1abc9c;
        font-size: 24px;
        margin-bottom: 1rem;
    }
    .sidebar-item {
        color: white;
        padding: 0.5rem 0;
        font-size: 16px;
        cursor: pointer;
        transition: all 0.2s ease-in-out;
    }
    .sidebar-item:hover {
        background-color: #34495e;
        padding-left: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.link-container {
    display: flex;
    justify-content: space-between;
    margin-bottom: 20px;
}

.link-card {
    flex: 1;
    background-color: #3498db;
    color: white;
    padding: 20px;
    margin-right: 10px;
    border-radius: 10px;
    font-family: Arial, sans-serif;
    min-height: 100px;
    position: relative;
}
.link-card:nth-child(2) { background-color: #e67e22; }
.link-card:nth-child(3) { background-color: #e74c3c; }
.link-card:nth-child(4) { background-color: #2ecc71; }

.link-title {
    font-weight: bold;
    font-size: 18px;
}

.link-desc {
    font-size: 14px;
    margin-top: 10px;
}

.link-icon {
    position: absolute;
    top: 10px;
    right: 10px;
    font-size: 25px;
}
</style>
""", unsafe_allow_html=True)

# HTML構造
st.markdown("""
<div class="link-container">
    <div class="link-card">
        <div class="link-title">Link1</div>
        <div class="link-desc">The description of the link here</div>
        <div class="link-icon">📁</div>
    </div>
    <div class="link-card">
        <div class="link-title">Link2</div>
        <div class="link-desc">The description of the link here</div>
        <div class="link-icon">📁</div>
    </div>
    <div class="link-card">
        <div class="link-title">Link3</div>
        <div class="link-desc">The description of the link here</div>
        <div class="link-icon">📁</div>
    </div>
    <div class="link-card">
        <div class="link-title">Link4</div>
        <div class="link-desc">The description of the link here</div>
        <div class="link-icon">📁</div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- サイドバーのレイアウト ---
with st.sidebar:
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.markdown('<h2>FREEworks</h2>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-item">🏠 Home</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-item">📄 New Report</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-item">📁 New Template</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-item">⭐ Favorite</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-item">📊 Template</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-item">🗃️ Data</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-item">📑 Report</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-item">⚙️ Settings</div>', unsafe_allow_html=True)
    st.markdown('<hr style="border:0.5px solid white;">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-item">👤 UserName</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def check_out_of_control(xbars, Rs, Ss, x_UCL, x_LCL, r_UCL, r_LCL, s_UCL, s_LCL):
    alert_flags = []
    for i in range(len(xbars)):
        if (
            xbars[i] > x_UCL or xbars[i] < x_LCL or
            Rs[i] > r_UCL or Rs[i] < r_LCL or
            Ss[i] > s_UCL or Ss[i] < s_LCL
        ):
            alert_flags.append(True)
        else:
            alert_flags.append(False)
    return alert_flags

def highlight_out_of_control_rows(df, group_size, alerts):
    def highlight_row(i):
        return ['background-color: pink'] * len(df.columns) if i else [''] * len(df.columns)

    flags = []
    for idx in range(len(df)):
        group_idx = idx // group_size
        flag = alerts[group_idx] if group_idx < len(alerts) else False
        flags.append(highlight_row(flag))
    return pd.DataFrame(flags, index=df.index, columns=df.columns)

import pandas as pd
import os
import time
from sklearn.ensemble import RandomForestClassifier

def AI_Simulator():

    # モデル学習
    X_train = pd.read_csv("X_future_deviation.csv")
    y_train = pd.read_csv("y_future_deviation.csv").values.ravel()
    model = RandomForestClassifier(n_estimators=100, max_depth=3, random_state=42)
    model.fit(X_train, y_train)

    # 監視ファイル
    CSV_FILE = "データ.csv"

    while True:
        try:
            if os.path.exists(CSV_FILE):
                df = pd.read_csv(CSV_FILE, sep="|", encoding="utf-8")
                df.columns = ["時刻", "規格値", "pH", "溶出時間", "作業員ID", "温度", "湿度", "ロット番号"]

                if len(df) >= 5:
                    latest_row = df.tail(1).drop(columns=["時刻"])
                    latest_encoded = pd.get_dummies(latest_row, columns=["作業員ID", "ロット番号"])
                    X_input = latest_encoded.reindex(columns=X_train.columns, fill_value=0)

                    prob = model.predict_proba(X_input)[0][1]

                    with open("latest_prob.json", "w", encoding="utf-8") as f:
                        json.dump({"prob": round(prob, 4)}, f)

        except Exception as e:
            print(f"[AI_Simulatorエラー] {e}")

        time.sleep(1)


# ファイルパスと設定
CSV_FILE_PATH = "データ.csv" 
GROUP_SIZE = 5  # 5個で1群
UPDATE_INTERVAL = 3  # 秒ごとに更新


# ヘッダー
st.title("💊 リアルタイム測定データ表示")
st.write(f"更新間隔: {UPDATE_INTERVAL} 秒")

#データ生成スレッドを一度だけ起動
if st.button("▶️ データ生成をバックグラウンドで開始"):
    if "thread_started" not in st.session_state:
        threading.Thread(target=run_prediction_loop, daemon=True).start()
        st.session_state.thread_started = True
        st.success("✅ データ生成スレッドを開始しました！")
    else:
        st.info("✅ すでにデータ生成中です。")

    if "ai_thread_started" not in st.session_state:
        threading.Thread(target=AI_Simulator, daemon=True).start()
        st.session_state.ai_thread_started = True
        st.success("✅ AIによる逸脱確率予測を開始しました！")

# --- データ生成用ボタン（Excel.py を並列実行） ---
if "start_time" in st.session_state:
    elapsed = time.time() - st.session_state["start_time"]
    if elapsed < 5:
        st.info(f"⏳ データ生成中… 自動更新まで {int(5 - elapsed)} 秒")
        time.sleep(1)
        st.rerun()
    else:
        del st.session_state["start_time"]  # 一度だけ実行するため削除

st.markdown("""
<div style='color:red; font-weight:bold; font-size:16px; margin-top:10px;'>
⚠ ボタンを押した後 <u>10秒以上待ってから画面を更新</u> してください。<br>
生成には少し時間がかかります。
</div>
""", unsafe_allow_html=True)

# CSV読み込み
@st.cache_data(ttl=1)  # 1秒ごとにキャッシュを更新
def load_data():
    if os.path.exists(CSV_FILE_PATH):
        df = pd.read_csv(CSV_FILE_PATH,sep="|", encoding="utf-8")
        df.columns = ["時刻", "規格値", "pH", "溶出時間","作業員ID","温度","湿度","ロット番号"]
        return df
    else:
        return pd.DataFrame(columns=["時刻", "規格値", "pH", "溶出時間","作業員ID","温度","湿度","ロット番号"])

df = load_data()

# 管理図の描画
if not df.empty and len(df) >= GROUP_SIZE:

    # データの準備
    df["規格値"] = pd.to_numeric(df["規格値"], errors="coerce")
    df = df.dropna(subset=["規格値"])
    groups = [
        df["規格値"].values[i:i + GROUP_SIZE]
        for i in range(0, len(df["規格値"]), GROUP_SIZE)
        if len(df["規格値"].values[i:i + GROUP_SIZE]) == GROUP_SIZE
    ]
    group_means = [sum(g) / GROUP_SIZE for g in groups]

import io
from matplotlib.figure import Figure

# ----------- データ準備（再利用） ------------
group_ranges = [max(g) - min(g) for g in groups]
group_stds = [pd.Series(g).std(ddof=1) for g in groups]

figsize_common = (4.5, 2.5)  # 横幅4.5, 縦幅2.5で統一

# ----------- X̄管理図 ------------
overall_mean = sum(group_means) / len(group_means)
std_dev = pd.Series(group_means).std()
UCL_xbar = overall_mean + 3 * std_dev
LCL_xbar = overall_mean - 3 * std_dev

fig_xbar = Figure(figsize_common, dpi=100)
ax1 = fig_xbar.subplots()
ax1.plot(group_means, marker='o', label='群平均', markersize=4)
ax1.axhline(UCL_xbar, color='r', linestyle='--', label='UCL')
ax1.axhline(LCL_xbar, color='b', linestyle='--', label='LCL')
ax1.axhline(overall_mean, color='g', linestyle='-', label='中心線')
ax1.set_title("X̄（エックスバー）管理図", fontsize=10)
ax1.set_xlabel("群番号", fontsize=8)
ax1.set_ylabel("規格値の平均", fontsize=8)
ax1.tick_params(labelsize=7)
ax1.legend(fontsize=7)
fig_xbar.tight_layout()

# ----------- R管理図 ------------
R_bar = sum(group_ranges) / len(group_ranges)
UCL_R = R_bar * 2.115  # n=5 → D4
LCL_R = R_bar * 0.000  # n=5 → D3

fig_r = Figure(figsize_common, dpi=100)
ax2 = fig_r.subplots()
ax2.plot(group_ranges, marker='s', label='範囲(R)', color='orange', markersize=4)
ax2.axhline(UCL_R, color='r', linestyle='--', label='UCL')
ax2.axhline(LCL_R, color='b', linestyle='--', label='LCL')
ax2.axhline(R_bar, color='g', linestyle='-', label='中心線')
ax2.set_title("R（レンジ）管理図", fontsize=10)
ax2.set_xlabel("群番号", fontsize=8)
ax2.set_ylabel("範囲", fontsize=8)
ax2.tick_params(labelsize=7)
ax2.legend(fontsize=7)
ax2.set_ylim(0, max(UCL_R * 1.1, max(group_ranges) * 1.1)) 
fig_r.tight_layout()
 # Y軸固定

# ----------- S管理図 ------------
S_bar = sum(group_stds) / len(group_stds)
UCL_S = S_bar * 2.089  # n=5 → B4
LCL_S = S_bar * 0.000  # n=5 → B3

fig_s = Figure(figsize_common, dpi=100)
ax3 = fig_s.subplots()
ax3.plot(group_stds, marker='^', label='標準偏差(S)', color='purple', markersize=4)
ax3.axhline(UCL_S, color='r', linestyle='--', label='UCL')
ax3.axhline(LCL_S, color='b', linestyle='--', label='LCL')
ax3.axhline(S_bar, color='g', linestyle='-', label='中心線')
ax3.set_title("S（標準偏差）管理図", fontsize=10)
ax3.set_xlabel("群番号", fontsize=8)
ax3.set_ylabel("標準偏差", fontsize=8)
ax3.tick_params(labelsize=7)
ax3.legend(fontsize=7)
ax3.set_ylim(0, max(UCL_S * 1.1, max(group_stds) * 1.1))  # Y軸固定
fig_s.tight_layout()

# ----------- Streamlit 表示 ------------
# 最新データと管理図を横並びに配置（左：表、右：縦に並んだグラフ）
# 表と管理図を左右に分ける（左：表、右：グラフ群）
# 最新データ（表形式で縦に表示）
st.markdown('<div class="section-header">最新データ</div>', unsafe_allow_html=True)
st.dataframe(df.tail(10).reset_index(drop=True), use_container_width=True)

# 管理図（R → X̄ → Sの順に縦並び）
st.markdown('<div class="section-header">管理図一覧</div>', unsafe_allow_html=True)

# 1行目の2列：R と X̄
row1_col1, row1_col2 = st.columns(2)

with row1_col2:
    buf_r = io.BytesIO()
    fig_r.savefig(buf_r, format="png", dpi=100)
    st.image(buf_r, caption="R（レンジ）管理図", use_container_width=True)

with row1_col1:
    buf_xbar = io.BytesIO()
    fig_xbar.savefig(buf_xbar, format="png", dpi=100)
    st.image(buf_xbar, caption="X̄（エックスバー）管理図", use_container_width=True)

# 2行目の2列：S と空欄
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    buf_s = io.BytesIO()
    fig_s.savefig(buf_s, format="png", dpi=100)
    st.image(buf_s, caption="S（標準偏差）管理図", use_container_width=True)

with row2_col2:
    st.markdown("#### 最新データと逸脱確率")
    latest_row = df.tail(1)
    st.dataframe(latest_row.reset_index(drop=True), use_container_width=True)

    try:
        with open("latest_prob.json", "r", encoding="utf-8") as f:
            prob = json.load(f)["prob"]
        st.metric("逸脱する確率", f"{prob * 100:.1f} %")
    except:
        st.warning("逸脱確率を読み込めませんでした。") # 空白スペース用のダミー（空欄）

alerts = check_out_of_control(group_means, group_ranges, group_stds, UCL_xbar, LCL_xbar, UCL_R, LCL_R, UCL_S, LCL_S)

# アラート表示（逸脱があれば）
alerts = check_out_of_control(group_means, group_ranges, group_stds,
                              UCL_xbar, LCL_xbar, UCL_R, LCL_R, UCL_S, LCL_S)

# --- セッション初期化（1回だけ） ---
if "was_out_of_control" not in st.session_state:
    st.session_state.was_out_of_control = False

# --- 今回の逸脱状態（any Trueなら逸脱） ---
is_now_out_of_control = any(alerts)

# --- 状態遷移の検出と警告表示 ---
# 条件：前回は正常 → 今回逸脱 → アラート表示
if is_now_out_of_control and not st.session_state.was_out_of_control:
    st.error("⚠ 管理図で逸脱（UCL超え／LCL割れ）を検出しました！")

    components.html("""
        <script>
            alert("⚠️ 警告：逸脱が検出されました！");
        </script>
    """, height=0)

st.session_state.was_out_of_control = is_now_out_of_control

if "deviation_history" not in st.session_state:
    st.session_state.deviation_history = pd.DataFrame(columns=df.columns)

existing_history = st.session_state.get("deviation_history", pd.DataFrame())

new_deviation_rows = pd.DataFrame()

for i, flag in enumerate(alerts):
    if flag:
        start_idx = i * GROUP_SIZE
        end_idx = start_idx + GROUP_SIZE
        new_rows = df.iloc[start_idx:end_idx]
        new_rows = new_rows[~new_rows["時刻"].isin(st.session_state.deviation_history["時刻"])]
        new_deviation_rows = pd.concat([new_deviation_rows, new_rows])

if not new_deviation_rows.empty:
    st.session_state.deviation_history = pd.concat(
        [st.session_state.deviation_history, new_deviation_rows]
    )

if not st.session_state.deviation_history.empty:
    st.markdown('<div class="section-header">過去の逸脱データ（累積）</div>', unsafe_allow_html=True)
    st.dataframe(st.session_state.deviation_history.reset_index(drop=True), use_container_width=True)
# 逸脱履歴のコピーを作成
df_to_download = st.session_state.deviation_history.copy()

# 1行目を削除（インデックス0の行）
df_to_download = df_to_download.iloc[1:].reset_index(drop=True)

# 列名を再設定（列の順番がずれていないことが前提）
df_to_download.columns = ["時刻", "規格値", "pH", "溶出時間", "作業員ID", "温度", "湿度", "ロット番号"]

# Excel形式に変換
excel_bytes = io.BytesIO()
with pd.ExcelWriter(excel_bytes, engine='xlsxwriter') as writer:
    df_to_download.to_excel(writer, index=False, sheet_name='逸脱データ')
excel_bytes.seek(0)

# ダウンロードボタンの表示
st.download_button(
    label="📥 逸脱データをExcel形式でダウンロード",
    data=excel_bytes,
    file_name="逸脱データ.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

if "start_time" in st.session_state:
    elapsed = time.time() - st.session_state["start_time"]
    if elapsed < 5:
        st.info(f"⏳ 自動更新まで {int(5 - elapsed)} 秒")
        time.sleep(1)
        st.rerun()
    else:
        del st.session_state["start_time"]
else:
    # ✅ 通常時は一定間隔で更新し続ける（必要なら）
    time.sleep(UPDATE_INTERVAL)
    st.rerun()



