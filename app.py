import streamlit as st
from rembg import remove
from PIL import Image, ImageEnhance, ImageFilter
import io

# ページ設定
st.set_page_config(page_title="manbo's EC Camera", layout="centered")

def process_image(uploaded_file, count):
    # 1. 画像読み込み
    img = Image.open(uploaded_file)
    
    # 2. 1200 x 1200pxにスクエアリサイズ（中央切り抜き）
    width, height = img.size
    min_dim = min(width, height)
    left = (width - min_dim) / 2
    top = (height - min_dim) / 2
    img = img.crop((left, top, left + min_dim, top + min_dim))
    img = img.resize((1200, 1200), Image.Resampling.LANCZOS)

    # 3. 背景ぼかし加工
    mask = remove(img, only_mask=True)
    background = img.filter(ImageFilter.GaussianBlur(radius=15))
    img.paste(background, (0, 0), mask=Image.eval(mask, lambda x: 255 - x))

    # 4. 色彩補正（売れるコントラスト）
    img = ImageEnhance.Contrast(img).enhance(1.3)
    img = ImageEnhance.Color(img).enhance(1.2)

    # 5. ファイル名
    file_name = f"food{str(count).zfill(2)}.jpg"
    return img, file_name

st.title("📸 manbo's EC Camera")
st.write("写真をアップロードするだけで、1200px・背景ぼかし・色調補正を自動で行います。")

uploaded_files = st.file_uploader("商品写真を選択してください", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)

if uploaded_files:
    for i, file in enumerate(uploaded_files):
        processed_img, name = process_image(file, i + 1)
        st.image(processed_img, caption=f"加工済み: {name}")
        
        buf = io.BytesIO()
        processed_img.save(buf, format="JPEG", quality=90)
        st.download_button(label=f"{name} をスマホに保存", data=buf.getvalue(), file_name=name, mime="image/jpeg")
