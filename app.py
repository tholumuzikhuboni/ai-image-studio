import streamlit as st
import vertexai
import io
import numpy as np
from datetime import datetime
from PIL import Image as PILImage
from google.cloud import storage, speech
from vertexai.preview.vision_models import ImageGenerationModel, Image as VertexImage
from st_audiorec import st_audiorec

# --- 1. CONFIGURATION ---
PROJECT_ID = "your-project-id"
LOCATION = "us-central1"
BUCKET_NAME = "your-bucket-name"

vertexai.init(project=PROJECT_ID, location=LOCATION)
model = ImageGenerationModel.from_pretrained("imagen-4.0-generate-001")
storage_client = storage.Client()
speech_client = speech.SpeechClient()

# --- 2. ADVANCED UI STYLING ---
st.set_page_config(page_title="Imagen Studio Pro", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #050505; color: #eee; }
    [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 1px solid #222; }
    .stButton>button { 
        width: 100%; border-radius: 8px; background: #ffffff; color: #000; 
        border: none; padding: 12px; font-weight: 600; 
    }
    .stTextArea textarea { background-color: #111 !important; border: 1px solid #333 !important; color: #eee !important; }
    .status-box { padding: 15px; border-radius: 8px; border: 1px solid #333; background: #111; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CORE LOGIC ---
def transcribe_audio(audio_bytes):
    audio = speech.RecognitionAudio(content=audio_bytes)
    config = speech.RecognitionConfig(encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16, language_code="en-US")
    response = speech_client.recognize(config=config, audio=audio)
    return " ".join([r.alternatives[0].transcript for r in response.results])

def save_and_upload(pil_img, prefix="studio"):
    buf = io.BytesIO()
    pil_img.save(buf, format='PNG')
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = f"generated/{prefix}_{ts}.png"
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(fname)
    blob.upload_from_string(buf.getvalue(), content_type="image/png")
    return blob.public_url

# --- 4. HEADER ---
st.title("Studio Professional")
st.markdown("<p style='color: #666;'>Advanced Image Synthesis & Generative Editing Suite</p>", unsafe_allow_html=True)

# --- 5. SIDEBAR: MODE & CONFIG ---
with st.sidebar:
    st.markdown("### Workspace Mode")
    mode = st.radio("Select Workflow", ["Text to Image", "Generative Edit", "Outpainting"])
    
    st.markdown("---")
    st.markdown("### Parameters")
    aspect_ratio = st.selectbox("Aspect Ratio", ["1:1", "4:3", "16:9"])
    
    st.markdown("---")
    st.markdown("### Voice Control")
    wav_audio_data = st_audiorec()
    voice_transcript = ""
    if wav_audio_data and st.button("Transcribe Command"):
        voice_transcript = transcribe_audio(wav_audio_data)

# --- 6. MAIN STUDIO ---
tab_work, tab_gallery = st.tabs(["Active Workspace", "Cloud Repository"])

with tab_work:
    col_ui, col_preview = st.columns([1, 1])

    with col_ui:
        prompt = st.text_area("Creative Command", value=voice_transcript, placeholder="Describe the desired result...", height=150)
        
        base_image = None
        mask_image = None

        if mode in ["Generative Edit", "Outpainting"]:
            st.markdown("### Source Asset")
            uploaded_file = st.file_uploader("Upload Image", type=['png', 'jpg', 'jpeg'])
            if uploaded_file:
                base_image = PILImage.open(uploaded_file).convert("RGB")
                st.image(base_image, caption="Base Image", width=250)
                
                if mode == "Generative Edit":
                    mask_file = st.file_uploader("Optional Mask (B&W PNG)", type=['png'])
                    if mask_file:
                        mask_image = PILImage.open(mask_file).convert("L")
                        st.image(mask_image, caption="Active Mask", width=250)

        if st.button("Execute Studio Command"):
            if not prompt:
                st.warning("Prompt is required.")
            else:
                with st.spinner("Processing Generative Task..."):
                    try:
                        if mode == "Text to Image":
                            response = model.generate_images(prompt=prompt, aspect_ratio=aspect_ratio)
                        
                        elif mode == "Generative Edit" and base_image:
                            # Convert PIL to Vertex Image
                            v_base = VertexImage(image_bytes=uploaded_file.getvalue())
                            v_mask = None
                            if mask_file:
                                v_mask = VertexImage(image_bytes=mask_file.getvalue())
                            
                            response = model.edit_image(
                                prompt=prompt,
                                base_image=v_base,
                                mask=v_mask
                            )
                        
                        elif mode == "Outpainting" and base_image:
                            v_base = VertexImage(image_bytes=uploaded_file.getvalue())
                            response = model.outpaint(
                                prompt=prompt,
                                base_image=v_base
                            )

                        # Output Processing
                        result_img = response.images[0]
                        st.session_state['latest_result'] = result_img._pil_image
                        save_and_upload(result_img._pil_image, prefix=mode.lower().replace(" ", "_"))
                        st.success("Task Complete. Asset committed to Cloud.")
                    
                    except Exception as e:
                        st.error(f"Studio Error: {e}")

    with col_preview:
        st.markdown("### Preview Rendering")
        if 'latest_result' in st.session_state:
            st.image(st.session_state['latest_result'], use_container_width=True)
        else:
            st.markdown("<div style='height: 400px; border: 1px dashed #333; display: flex; align-items: center; justify-content: center; color: #444;'>No Active Rendering</div>", unsafe_allow_html=True)

with tab_gallery:
    st.markdown("### Synchronized Assets")
    try:
        blobs = storage_client.list_blobs(BUCKET_NAME, prefix="generated/", max_results=12)
        grid = st.columns(4)
        for i, blob in enumerate(blobs):
            with grid[i % 4]:
                st.image(blob.public_url)
                st.markdown(f"<small style='color:#555;'>{blob.name.split('/')[-1]}</small>", unsafe_allow_html=True)
    except Exception:
        st.info("Repository empty.")
