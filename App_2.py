import streamlit as st
import os
import json
from streamlit_drawable_canvas import st_canvas

# =====================
# 1. 初期設定とフォルダ作成
# =====================
SAVE_DIR = "memos"
os.makedirs(SAVE_DIR, exist_ok=True)

st.set_page_config(page_title="デジタル備忘録", layout="wide")
st.title("🖊️ デジタル備忘録（手書き・保存対応）")

# セッション状態の初期化
if "selected_file" not in st.session_state:
    st.session_state["selected_file"] = "新規作成"

# =====================
# 2. サイドバー：メモ一覧と検索
# =====================
st.sidebar.header("🗂️ メモ一覧")
files = os.listdir(SAVE_DIR)
search_query = st.sidebar.text_input("検索", "")

# 検索フィルタリング
display_files = []
for f in files:
    if f.endswith(".json"):
        if search_query.lower() in f.lower():
            display_files.append(f)

selection = st.sidebar.selectbox(
    "編集するメモを選択",
    ["新規作成"] + display_files,
    index=0 if st.session_state["selected_file"] not in display_files else display_files.index(st.session_state["selected_file"]) + 1
)
st.session_state["selected_file"] = selection

# =====================
# 3. データの読み込み
# =====================
# デフォルト値の設定
current_data = {"title": "", "tags": "", "text": "", "drawing": None}

if st.session_state["selected_file"] != "新規作成":
    with open(os.path.join(SAVE_DIR, st.session_state["selected_file"]), "r", encoding="utf-8") as f:
        current_data = json.load(f)

# =====================
# 4. 入力フォームの作成
# =====================
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 テキスト情報")
    input_title = st.text_input("タイトル", value=current_data.get("title", ""))
    input_tags = st.text_input("タグ（カンマ区切り）", value=current_data.get("tags", ""))
    input_text = st.text_area("本文", value=current_data.get("text", ""), height=200)

with col2:
    st.subheader("🎨 手書きキャンバス")
    # キャンバスの設定
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",  # 塗りつぶし色
        stroke_width=3,
        stroke_color="#000000",
        background_color="#eeeeee",
        initial_drawing=current_data.get("drawing") if st.session_state["selected_file"] != "新規作成" else None,
        update_streamlit=True,
        height=300,
        key="canvas",
    )

# =====================
# 5. 保存・更新処理
# =====================
st.divider()
if st.button("💾 メモを保存する"):
    if not input_title:
        st.error("タイトルを入力してください。")
    else:
        # 保存するデータの作成
        save_data = {
            "title": input_title,
            "tags": input_tags,
            "text": input_text,
            "drawing": canvas_result.json_data  # キャンバスの描画データをJSONとして保存
        }
        
        # ファイル名の決定（タイトルをファイル名にする）
        file_path = os.path.join(SAVE_DIR, f"{input_title}.json")
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(save_data, f, ensure_ascii=False, indent=4)
        
        st.success(f"保存しました: {input_title}")
        st.rerun() # 画面を更新して一覧に反映
