TRASH_DIR = "trash"
os.makedirs(TRASH_DIR, exist_ok=True)
import shutil

shutil.move(
    os.path.join(SAVE_DIR, st.session_state["selected"]),
    os.path.join(TRASH_DIR, st.session_state["selected"])
)
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



import streamlit as st
import os
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import json

st.title("デジタル備忘録（手書き対応）")

SAVE_DIR = "memos"
os.makedirs(SAVE_DIR, exist_ok=True)

# ===== ファイル選択 =====
all_files = os.listdir(SAVE_DIR)

files = []
for file in all_files:
    try:
        with open(os.path.join(SAVE_DIR, file), "r", encoding="utf-8") as f:
            data = json.load(f)
            target = (
                data.get("title", "") +
                " ".join(data.get("tags", [])) +
                data.get("text", "")
            )
            if query.lower() in target.lower():
                files.append(file)
    except:
        pass
st.subheader("🔍 検索結果")

if not results:
    st.caption("該当するメモはありません")
else:
    for item in results:
        with st.container():
            st.markdown(f"### {item['title']}")
            st.caption("タグ: " + ", ".join(item["tags"]))

            if st.button("開く", key=item["file"]):
                st.session_state["selected"] = item["file"]
                st.experimental_rerun()
if not query:
    selected = st.selectbox(
        "編集するメモを選ぶ",
        ["新規"] + os.listdir(SAVE_DIR),
        key="selected"
    )
else:
    selected = st.session_state.get("selected", "新規")
if st.button("開く", key=item["file"]):
    st.session_state["selected"] = item["file"]
    st.experimental_rerun()

if st.session_state.get("selected") == "新規":
    filename = st.text_input(
        "ファイル名（例：memo1.json）",
        key="filename"
    )
    title = st.text_input("タイトル", key="title")
    tags_input = st.text_input("タグ（カンマ区切り）")
    tags = [t.strip() for t in tags_input.split(",") if t.strip()]
    text = ""
else:
    # 既存ファイル読み込み（今までの処理）


text = ""
canvas_data = None
filename = ""

if selected != "新規":
    filename = selected
    with open(os.path.join(SAVE_DIR, filename), "r", encoding="utf-8") as f:
        data = json.load(f)
title = data.get("title", "")
tags = data.get("tags", [])
text = data.get("text", "")
canvas_data = data.get("drawing", None)

else:
    filename = st.text_input("ファイル名（例：memo1.json）")

results = []

for file in os.listdir(SAVE_DIR):
    try:
        with open(os.path.join(SAVE_DIR, file), "r", encoding="utf-8") as f:
            data = json.load(f)

        target = (
            data.get("title", "") +
            " ".join(data.get("tags", [])) +
            data.get("text", "")
        )

        if query.lower() in target.lower():
            results.append({
                "file": file,
                "title": data.get("title", "（無題）"),
                "tags": data.get("tags", [])
            })
    except:
        pass


# ===== キーボード入力 =====
title = st.text_input("タイトル", value=title)

tags_input = st.text_input(
    "タグ（カンマ区切り）",
    value=", ".join(tags)
)
tags = [t.strip() for t in tags_input.split(",") if t.strip()]

content = st.text_area("キーボード入力", value=text, height=150)

# ===== 手書き入力 =====
st.subheader("手書きメモ")
canvas = st_canvas(
    fill_color="rgba(0, 0, 0, 0)",
    stroke_width=3,
    stroke_color="#000000",
    background_color="#FFFFFF",
    height=300,
    width=500,
    drawing_mode="freedraw",
    key="canvas",
)

# ===== 自動保存 =====
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

import json

if st.session_state.get("confirm_delete"):
    st.error("本当に削除しますか？（元に戻せません）")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("はい、削除する"):
            file_path = os.path.join(SAVE_DIR, st.session_state["selected"])
            if os.path.exists(file_path):
                os.remove(file_path)

            st.success("削除しました")

            # 状態リセット
            st.session_state["selected"] = "新規"
            st.session_state["confirm_delete"] = False
            st.session_state["filename"] = ""
            st.session_state["title"] = ""
            st.session_state["tags"] = []
            st.session_state["text"] = ""

    with col2:
        if st.button("キャンセル"):
            st.session_state["confirm_delete"] = False

