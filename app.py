import streamlit as st
import io
import os
import random
from datetime import datetime
from PIL import Image as PILImage
from google import genai
from google.genai import types
from google.cloud import storage

# --- 1. CONFIGURATION ---
PROJECT_ID = "YOUR_PROJECT_ID"
LOCATION = "us-central1"
BUCKET_NAME = "YOUR_BUCKET_NAME"

# Initialize the new 2026 Client
client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)
storage_client = storage.Client()

# --- 2. UI & STYLE ---
st.set_page_config(page_title="Imagen Studio", layout="centered")
st.title("Imagen Studio")

st.markdown("""
    <style>
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; text-align: center; color: #666; padding: 10px; font-size: 12px; }
    </style>
    <div class="footer">Built by Tholumuzi © 2026</div>
    """, unsafe_allow_html=True)

# --- 3. UTILS ---
def upload_to_cloud(pil_img):
    buf = io.BytesIO()
    pil_img.save(buf, format='PNG')
    fname = f"gen/asset_{datetime.now().strftime('%H%M%S')}.png"
    blob = storage_client.bucket(BUCKET_NAME).blob(fname)
    blob.upload_from_string(buf.getvalue(), content_type="image/png")
    return blob.public_url

# --- 4. WORKSPACE ---
with st.sidebar:
    st.header("Controls")
    mode = st.selectbox("Action", ["Generate", "Smart Edit", "Expand", "Remove Background"])
    
    aspect_ratio_val = "1:1"
    if mode == "Generate":
        st.subheader("Generation Settings")
        aspect_ratio_val = st.selectbox("Aspect Ratio", ["1:1", "16:9", "4:3", "9:16"])
    
    st.subheader("Advanced Settings")
    negative_prompt = st.text_area("Negative Prompt", placeholder="e.g., pink text, altered colors, unreadable, distorted")

base_image = None
img_bytes = None
if mode in ["Smart Edit", "Expand", "Remove Background"]:
    up = st.file_uploader("Upload Image", type=['png', 'jpg', 'jpeg'])
    if up:
        base_image = PILImage.open(up)
        img_bytes = up.getvalue()
        st.image(base_image, width=300, caption="Source Asset")

if "placeholder" not in st.session_state:
    placeholders = [
        "A futuristic cyberpunk cityscape at night...",
        "Change the background to a sunny tropical beach...",
        "Make the image look like a watercolor painting...",
        "Add a flying car in the sky...",
        "A photorealistic portrait of a dog wearing a top hat..."
    ]
    st.session_state["placeholder"] = random.choice(placeholders)

prompt = st.text_area("Creative Command", placeholder=st.session_state["placeholder"])

if st.button("Generate", type="primary"):
    if not prompt and mode != "Remove Background":
        st.error("Prompt required.")
    else:
        with st.spinner("Processing..."):
            try:
                if mode == "Generate":
                    # IMAGEN 4.0 (Latest 2026 Generation)
                    gen_args = {"number_of_images": 1, "aspect_ratio": aspect_ratio_val}
                    if negative_prompt:
                        gen_args["negative_prompt"] = negative_prompt
                    response = client.models.generate_images(
                        model="imagen-4.0-generate-001",
                        prompt=prompt,
                        config=types.GenerateImagesConfig(**gen_args)
                    )
                
                elif mode == "Smart Edit" and base_image:
                    # SMART WORKFLOW (Vision-based zero-shot editing)
                    # Protects original color palette and lighting automatically
                    smart_negative = "altered colors, changed lighting, modified style, different color palette"
                    final_negative = f"{negative_prompt}, {smart_negative}" if negative_prompt else smart_negative

                    response = client.models.edit_image(
                        model="imagen-3.0-capability-001",
                        prompt=prompt,
                        reference_images=[
                            types.RawReferenceImage(
                                reference_image=types.Image(image_bytes=img_bytes),
                                reference_id=0
                            )
                        ],
                        config=types.EditImageConfig(**{
                            "edit_mode": "EDIT_MODE_DEFAULT",
                            "number_of_images": 1,
                            "negative_prompt": final_negative
                        })
                    )

                elif mode == "Expand" and base_image:
                    # OUTPAINTING (Mask-free canvas expansion)
                    response = client.models.edit_image(
                        model="imagen-3.0-capability-001",
                        prompt=prompt,
                        reference_images=[
                            types.RawReferenceImage(
                                reference_image=types.Image(image_bytes=img_bytes),
                                reference_id=0
                            )
                        ],
                        config=types.EditImageConfig(**{
                            "edit_mode": "EDIT_MODE_OUTPAINT",
                            "number_of_images": 1,
                            **({"negative_prompt": negative_prompt} if negative_prompt else {})
                        })
                    )

                elif mode == "Remove Background" and base_image:
                    # BGEP / No Background implementation
                    bg_prompt = prompt if prompt else "pure white studio background, plain, seamless"
                    response = client.models.edit_image(
                        model="imagen-3.0-capability-001",
                        prompt=bg_prompt,
                        reference_images=[
                            types.RawReferenceImage(
                                reference_image=types.Image(image_bytes=img_bytes),
                                reference_id=0
                            ),
                            types.MaskReferenceImage(
                                reference_id=1,
                                config=types.MaskReferenceConfig(
                                    mask_mode="MASK_MODE_BACKGROUND"
                                )
                            )
                        ],
                        config=types.EditImageConfig(**{
                            "edit_mode": "EDIT_MODE_INPAINT_INSERTION",
                            "number_of_images": 1,
                            **({"negative_prompt": negative_prompt} if negative_prompt else {})
                        })
                    )

                # Fetch and Display
                final_img = response.generated_images[0].image
                final_pil_img = PILImage.open(io.BytesIO(final_img.image_bytes))
                st.session_state['out'] = final_pil_img
                upload_to_cloud(final_pil_img)
                st.success("Task Complete.")

            except Exception as e:
                st.error(f"Studio Error: {e}")

if 'out' in st.session_state:
    st.divider()
    st.image(st.session_state['out'], use_container_width=True)
