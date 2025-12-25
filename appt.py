import streamlit as st
from googletrans import Translator, LANGUAGES
from gtts import gTTS
import io
import base64
import streamlit.components.v1 as components

# -------------------- Streamlit Setup --------------------
st.set_page_config(page_title="🌐 Smart Translator+", page_icon="🌍", layout="centered")

st.title("🌐 Smart Translator+")
st.write("Translate any text into your desired language, with auto-detect and voice output 🔊")

translator = Translator()

# -------------------- Input --------------------
text_to_translate = st.text_area("Enter text to translate:", height=150, placeholder="Type or paste text here...")

# Target language selector
target_lang = st.selectbox(
    "Select target language:",
    options=list(LANGUAGES.keys()),
    format_func=lambda x: LANGUAGES[x].capitalize()
)

# -------------------- Translate --------------------
if st.button("🔁 Translate"):
    if text_to_translate.strip():
        # Detect language
        detected = translator.detect(text_to_translate)
        detected_lang_name = LANGUAGES.get(detected.lang, "Unknown").capitalize()

        # Perform translation
        translated = translator.translate(text_to_translate, dest=target_lang)

        st.success(f"✅ Detected Language: {detected_lang_name}")
        st.markdown("### 🈸 Translated Text:")
        st.text_area("", translated.text, height=150)

        # -------------------- Copy Button --------------------
                # --- Copy Button (JS) ---
        copy_code = f"""
            <script>
            function copyToClipboard() {{
                var text = `{translated.text}`;
                navigator.clipboard.writeText(text);
                alert("✅ Text copied to clipboard!");
            }}
            </script>
            <button onclick="copyToClipboard()" 
                style="
                    background-color:#4CAF50;
                    color:white;
                    border:none;
                    padding:8px 16px;
                    border-radius:6px;
                    cursor:pointer;
                    font-size:16px;">
                📋 Copy Text
            </button>
        """
        components.html(copy_code, height=70)

        # -------------------- Text-to-Speech --------------------
        st.markdown("### 🔊 Listen to Translation:")
        tts = gTTS(text=translated.text, lang=target_lang)
        audio_bytes = io.BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)

        st.audio(audio_bytes, format="audio/mp3")

        # Download option
        b64 = base64.b64encode(audio_bytes.read()).decode()
        href = f'<a href="data:audio/mp3;base64,{b64}" download="translation.mp3">🎧 Download Audio</a>'
        st.markdown(href, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Please enter some text first.")

# -------------------- Footer --------------------
st.markdown("---")
st.caption("🌍 Smart Translator+ — built with Streamlit, Googletrans, and gTTS")
