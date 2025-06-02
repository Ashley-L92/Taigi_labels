import streamlit as st
import requests
import uuid
from PIL import Image
import base64

# === CONFIG ===
HUGGINGFACE_API_KEY = st.secrets["HUGGINGFACE_API_KEY"]
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/ylac/taigi-tts"


# === FUNCTION ===

def generate_safe_filename():
    return str(uuid.uuid4()) + ".mp3"

def text_to_taiwanese_tts(text):
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {"inputs": text}
    try:
        response = requests.post(HUGGINGFACE_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.content
    except Exception as e:
        st.error(f"語音合成失敗：{e}")
        return None

def play_audio(audio_bytes, label="語音播放"):
    audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
    audio_html = f"""
        <audio controls>
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
        </audio>
    """
    st.markdown(f"#### {label}")
    st.markdown(audio_html, unsafe_allow_html=True)

def summarize_image(image: Image.Image):
    # 🧪 模擬圖像辨識與總結，請換成實際處理
    return "這是一個模擬的商品標籤摘要，用於展示台語語音合成功能。"

# === APP UI ===

st.title("🛍️ 商品標籤解讀器（含台語語音）")

lang_option = st.radio("選擇語音語言", ["中文", "台語"], horizontal=True)
advance_mode = st.checkbox("進階模式")
uploaded_images = st.file_uploader("上傳商品標籤圖片", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if st.button("重新開始"):
    st.session_state.clear()
    st.rerun()

if uploaded_images:
    for idx, uploaded_file in enumerate(uploaded_images):
        try:
            image = Image.open(uploaded_file)
            st.image(image, caption=f"圖片 {idx+1}", use_column_width=True)

            summary = summarize_image(image)
            st.markdown(f"**總結：** {summary}")

            # 語音合成
            if lang_option == "中文":
                from gtts import gTTS
                tts = gTTS(summary, lang='zh')
                filename = generate_safe_filename()
                tts.save(filename)
                with open(filename, "rb") as f:
                    audio_bytes = f.read()
            else:  # 台語語音
                audio_bytes = text_to_taiwanese_tts(summary)

            if audio_bytes:
                play_audio(audio_bytes, label=f"圖片 {idx+1} 語音")

            if advance_mode:
                st.info("🔍 進階模式：可提供更多圖像細節與建議（尚未實作）")

        except Exception as e:
            st.error(f"處理圖片 {idx+1} 時發生錯誤：{e}")

