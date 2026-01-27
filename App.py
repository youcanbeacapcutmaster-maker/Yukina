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
    except:
        pass

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
    with open(os.path.join(SAVE_DIR, filename), "r", encoding="utf-8") as f:
        data = json.load(f)

    title = data.get("title", "")
    tags = data.get("tags", [])
    text = data.get("text", "")
    drawing = data.get("drawing", None)
else:
    filename = st.text_input("ファイル名（例：memo1.json）")
    title = ""
    tags = []
    text = ""
    drawing = None

# =====================
# 入力UI
# =====================
title = st.text_input("タイトル", value=title)

tags_input = st.text_input(
    "タグ（カンマ区切り）",
    value=", ".join(tags)
)
tags = [t.strip() for t in tags_input.split(",") if t.strip()]

content = st.text_area(
    "キーボード入力",
    value=text,
    height=150
)

st.subheader("✍ 手書きメモ")
canvas = st_canvas(
    fill_color="rgba(0,0,0,0)",
    stroke_width=3,
    stroke_color="#000000",
    background_color="#FFFFFF",
    height=300,
    width=500,
    drawing_mode="freedraw",
    key="canvas"
)

# =====================
# 自動保存
# =====================
if filename:
    save_data = {
        "title": title,
        "tags": tags,
        "text": content,
        "drawing": canvas.json_data
    }

    with open(os.path.join(SAVE_DIR, filename), "w", encoding="utf-8") as f:
        json.dump(save_data, f, ensure_ascii=False)

    st.success("自動保存中")

# =====================
# 削除 → ゴミ箱
# =====================
if selected != "新規":
    if st.button("🗑 ゴミ箱に移動"):
        shutil.move(
            os.path.join(SAVE_DIR, selected),
            os.path.join(TRASH_DIR, selected)
        )
        st.session_state["selected"] = "新規"
        st.experimental_rerun()

# =====================
# ゴミ箱
# =====================
st.subheader("🗑 ゴミ箱")

trash_files = os.listdir(TRASH_DIR)

if trash_files:
    trash_selected = st.selectbox(
        "復元するメモを選択",
        trash_files
    )

    if st.button("♻ 復元する"):
        shutil.move(
            os.path.join(TRASH_DIR, trash_selected),
            os.path.join(SAVE_DIR, trash_selected)
        )
        st.success("復元しました")
else:
    st.caption("ゴミ箱は空です")
