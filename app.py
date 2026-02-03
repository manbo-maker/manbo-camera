import streamlit as st
from PIL import Image, ImageEnhance
import io

# ページ設定
st.set_page_config(page_title="manbo's EC Camera Lite", layout="centered")

def process_image(uploaded_file, count):
    # 1. 画像読み込み & 形式変換（エラー回避用）
    img = Image.open(uploaded_file).convert("RGB")
    
    # 2. 1200 x 1200pxにスクエアリサイズ（中央切り抜き）
    width, height = img.size
    min_dim = min(width, height)
    left = (width - min_dim) / 2
    top = (height - min_dim) / 2
    img = img.crop((left, top, left + min_dim, top + min_dim))
    img = img.resize((1200, 1200), Image.Resampling.LANCZOS)

    # 3. 色彩補正（売れるコントラスト & 彩度アップ）
    img = ImageEnhance.Contrast(img).enhance(1.3) # コントラスト30%アップ
    img = ImageEnhance.Color(img).enhance(1.2)    # 彩度20%アップ

    # 4. ファイル名 (food01, food02...)
    file_name = f"food{str(count).zfill(2)}.jpg"
    return img, file_name

st.title("📸 manbo's EC Camera (Lite)")
st.write("1200pxリサイズ・色彩補正・自動命名を行います。")

uploaded_files = st.file_uploader("商品写真を選択してください", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)

if uploaded_files:
    for i, file in enumerate(uploaded_files):
        processed_img, name = process_image(file, i + 1)
        st.image(processed_img, caption=f"加工済み: {name}")
        
        # 保存処理（ここでエラーが起きないように修正済み）
        buf = io.BytesIO()
        processed_img.save(buf, format="JPEG", quality=90)
        st.download_button(label=f"{name} をスマホに保存", data=buf.getvalue(), file_name=name, mime="image/jpeg")
