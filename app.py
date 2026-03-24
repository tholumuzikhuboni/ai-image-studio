import streamlit as st
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel

# --- 1. CONFIGURATION ---
# We use the Project ID from your Google Cloud Dashboard.
# Location is set to us-central1 as it supports the latest Imagen 4 model.
PROJECT_ID = "your-project-id" 
LOCATION = "us-central1"

# Initialize the Vertex AI SDK to connect our app to Google Cloud
vertexai.init(project=PROJECT_ID, location=LOCATION)

# Load the Imagen 4 model - Google's state-of-the-art image generator
model = ImageGenerationModel.from_pretrained("imagen-4.0-generate-001")

# --- 2. UI SETUP ---
# Configure the page to use the full width of the browser for a professional look
st.set_page_config(page_title="Professional Image Studio", layout="wide")

# Custom CSS to improve the look of buttons and inputs (clean, no-emoji style)
st.markdown("""
    <style>
    .main { background-color: #fcfcfc; }
    .stButton>button { 
        width: 100%; 
        background-color: #1a73e8; 
        color: white; 
        border-radius: 4px; 
        border: none; 
        height: 3rem; 
    }
    .stTextInput>div>div>input { border-radius: 4px; }
    </style>
    """, unsafe_allow_html=True)

st.title("AI Visual Asset Generator")
st.write("Utilizing Imagen 4 via Vertex AI to generate commercial-grade imagery.")

# --- 3. SIDEBAR CONTROLS ---
# Using a sidebar keeps the main screen clean for the generated results
with st.sidebar:
    st.header("Image Specifications")
    aspect_ratio = st.selectbox("Aspect Ratio", ["1:1", "4:3", "16:9"])
    image_style = st.selectbox("Style Preset", ["Photorealistic", "Studio Lighting", "Flat Design"])

# --- 4. MAIN INTERFACE ---
# The text area where the user inputs their creative vision
prompt = st.text_area("Enter your creative brief:", placeholder="A modern architectural structure in Johannesburg at dusk...")

# The Action: What happens when the user clicks 'Generate'
if st.button("Generate Asset"):
    if prompt:
        with st.spinner("Communicating with Vertex AI API..."):
            # We combine the user prompt with the selected style for better results
            enhanced_prompt = f"{prompt}, {image_style}, high resolution, 8k"
            
            try:
                # Call the Imagen 4 API
                response = model.generate_images(
                    prompt=enhanced_prompt,
                    number_of_images=1,
                    aspect_ratio=aspect_ratio
                )
                
                # Display the image using the non-deprecated 'use_container_width'
                st.image(response.images[0]._pil_image, use_container_width=True)
                st.success("Asset generation complete.")
                
            except Exception as e:
                # Catching errors (like API permissions or billing issues)
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please provide a prompt to proceed.")
