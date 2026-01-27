import streamlit
import streamlit as st
import os
import json
import shutil
from streamlit_drawable_canvas import st_canvas

# =====================
# 初期設定
# =====================
SAVE_DIR = "memos"
TRASH_DIR = "trash"

os.makedirs(SAVE_DIR, exist_ok=True)
os.makedirs(TRASH_DIR, exist_ok=True)

if "selected" not in st.session_state:
    st.session_state["selected"] = "新規"

# =====================
# タイトル
# =====================
st.title("デジタル備忘録（手書き対応）")

# =====================
# 検索
# =====================
query = st.text_input("検索")
results = []

for file in os.listdir(SAVE_DIR):
    try:
        with open(os.path.join(SAVE_DIR, file), "r", encoding="utf-8") as f:
            data = json.load(f)

        target = (
            data.get("title", "")
            + " ".join(data.get("tags", []))
            + data.get("text", "")
        )

        if query.lower() in target.lower():
            results.append({
                "file": file,
                "title": data.get("title", "（無題）"),
                "tags": data.get("tags", [])
            })
    except Exception:
        continue

st.subheader("🔍 検索結果")

if query:
    if not results:
        st.caption("該当するメモはありません")
    else:
        for item in results:
            st.markdown(f"### {item['title']}")
            st.caption("タグ: " + ", ".join(item["tags"]))
            if st.button("開く", key=f"open_{item['file']}"):
                st.session_state["selected"] = item["file"]
                st.experimental_rerun()

# =====================
# メモ選択
# =====================
if not query:
    st.session_state["selected"] = st.selectbox(
        "編集するメモを選ぶ",
        ["新規"] + os.listdir(SAVE_DIR),
        index=0
    )

selected = st.session_state["selected"]

# =====================
# データ読み込み
# =====================
if selected != "新規":
    filename = selected
    try:
        with open(os.path.join(SAVE_DIR, filename), "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        data = {}

    title = data.get("title", "")
    tags = data.get("tags", [])
    text = data.get("text", "")
    drawing = data.get("drawing", None)
else:
    filename = st.text_input("ファイル名（例：memo1.json）")
    title = ""
