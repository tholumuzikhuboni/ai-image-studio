import streamlit as st
import vertexai
import io
import base64
from datetime import datetime
from google.cloud import storage, speech
from vertexai.preview.vision_models import ImageGenerationModel
from st_audiorec import st_audiorec

# --- 1. CONFIGURATION ---
PROJECT_ID = "your-project-id"
LOCATION = "us-central1"
BUCKET_NAME = "your-bucket-name"

vertexai.init(project=PROJECT_ID, location=LOCATION)
model = ImageGenerationModel.from_pretrained("imagen-4.0-generate-001")
storage_client = storage.Client()
speech_client = speech.Client()

# --- 2. UI STYLING ---
st.set_page_config(page_title="Imagen 4 Studio", layout="wide")

def local_css():
    st.markdown("""
        <style>
        /* Import Inter font for a professional look */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            background-color: #050505;
        }

        /* Glassmorphism sidebar */
        [data-testid="stSidebar"] {
            background-color: #0a0a0a;
            border-right: 1px solid #222;
        }

        /* Custom Button */
        .stButton>button {
            width: 100%;
            border-radius: 8px;
            background: #ffffff;
            color: #000000;
            border: none;
            padding: 12px;
            font-weight: 600;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background: #e0e0e0;
            transform: translateY(-1px);
        }

        /* Input styling */
        .stTextArea textarea, .stTextInput input {
            background-color: #111 !important;
            border: 1px solid #333 !important;
            color: #eee !important;
            border-radius: 8px !important;
        }

        /* Asset Card */
        .asset-card {
            background: #111;
            border: 1px solid #222;
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 20px;
        }
        
        /* Hide Streamlit Branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)

local_css()

# --- 3. ICON HELPERS (SVG) ---
ICON_MIC = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" x2="12" y1="19" y2="22"/></svg>'
ICON_GENERATE = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21 2-2 2m-7.61 7.61a5.5 5.5 0 1 1-7.778 7.778 5.5 5.5 0 0 1 7.777-7.777zm0 0L15.5 7.5m0 0 3 3L22 7l-3-3y-3.5"/></svg>'

# --- 4. APP LOGIC ---
def transcribe_audio(audio_bytes):
    audio = speech.RecognitionAudio(content=audio_bytes)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code="en-US",
    )
    response = speech_client.recognize(config=config, audio=audio)
    return " ".join([r.alternatives[0].transcript for r in response.results])

# HEADER
st.markdown(f"<h1>Imagen Studio 4.0 Professional</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #666; margin-bottom: 40px;'>Enterprise image synthesis for high-fidelity visual assets.</p>", unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.markdown("### Configuration")
    aspect_ratio = st.selectbox("Resolution / Ratio", ["1:1", "4:3", "16:9", "9:16"])
    sample_count = st.slider("Batch Size", 1, 4, 1)
    
    st.markdown("---")
    st.markdown(f"### {ICON_MIC} Voice Command", unsafe_allow_html=True)
    wav_audio_data = st_audiorec()
    
    voice_transcript = ""
    if wav_audio_data is not None:
        if st.button("Process Audio"):
            with st.spinner("Processing..."):
                voice_transcript = transcribe_audio(wav_audio_data)

# TABS
tab_gen, tab_lib = st.tabs(["Generation Engine", "Cloud Repository"])

with tab_gen:
    col_input, col_info = st.columns([2, 1])
    
    with col_input:
        prompt = st.text_area(
            "Creative Specification", 
            value=voice_transcript if voice_transcript else "",
            placeholder="Detailed description of visual subject, environment, and lighting...",
            height=180
        )
    
    with col_info:
        st.markdown("### Parameters")
        negative_prompt = st.text_input("Exclusion Criteria", placeholder="e.g. text, watermark, blur")
        style_preset = st.selectbox("Aesthetic", ["Natural", "Cinematic", "Flat Illustration", "Digital Art"])

    if st.button("Execute Generation"):
        if prompt:
            with st.spinner("Synchronizing with Vertex AI..."):
                try:
                    response = model.generate_images(
                        prompt=f"{prompt}, {style_preset}",
                        number_of_images=sample_count,
                        aspect_ratio=aspect_ratio,
                        negative_prompt=negative_prompt if negative_prompt else None
                    )
                    
                    st.markdown("### Output")
                    cols = st.columns(len(response.images))
                    for idx, img in enumerate(response.images):
                        cols[idx].image(img._pil_image, use_container_width=True)
                        
                        # Upload Logic
                        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                        fname = f"generated/asset_{ts}_{idx}.png"
                        img_byte_arr = io.BytesIO()
                        img._pil_image.save(img_byte_arr, format='PNG')
                        
                        bucket = storage_client.bucket(BUCKET_NAME)
                        blob = bucket.blob(fname)
                        blob.upload_from_string(img_byte_arr.getvalue(), content_type="image/png")
                    
                    st.toast("Success: Assets committed to Cloud Storage")
                except Exception as e:
                    st.error(f"Execution Error: {e}")
        else:
            st.warning("Specification required for generation.")

with tab_lib:
    st.markdown("### Synchronized Assets")
    try:
        blobs = storage_client.list_blobs(BUCKET_NAME, prefix="generated/", max_results=12)
        grid = st.columns(4)
        for i, blob in enumerate(blobs):
            with grid[i % 4]:
                st.markdown(f'<div class="asset-card">', unsafe_allow_html=True)
                st.image(blob.public_url)
                st.markdown(f"<small>{blob.name.split('/')[-1]}</small>", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
    except Exception:
        st.info("No assets found in the repository.")
