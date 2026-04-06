# 🎨 Imagen 4 Studio – AI Visual Asset Generator

A production-ready AI application that allows you to generate high-quality images using Google Vertex AI (Imagen 4), upload assets to Cloud Storage, and even generate prompts using **speech-to-text**.

---

# ⚠️ Important (Read First)

Before starting:

- You MUST have a Google Cloud account
- This project uses **paid Google Cloud services**
- Charges may occur depending on usage

👉 It is strongly recommended to:
- Sign up for the **free trial**: https://cloud.google.com/free
- Monitor billing in: https://console.cloud.google.com/billing

---

# 🚀 Step 1: Create a Google Cloud Project

1. Go to 👉 https://console.cloud.google.com/
2. Click **Select Project → New Project**
3. Enter a project name
4. Click **Create**
5. Select your new project

---

# 🔧 Step 2: Enable Required APIs

Open **Cloud Shell** and run:

```bash
gcloud services enable aiplatform.googleapis.com run.googleapis.com cloudbuild.googleapis.com storage.googleapis.com speech.googleapis.com
```

---

# 📦 Step 3: Create a Cloud Storage Bucket

```bash
gcloud storage buckets create gs://YOUR_BUCKET_NAME --location=us-central1
```

Make it public (for viewing images):

```bash
gsutil iam ch allUsers:objectViewer gs://YOUR_BUCKET_NAME
```

---

# 🧠 Step 4: Project Setup

Create project folder:

```bash
mkdir imagen-studio && cd imagen-studio
```

---

## requirements.txt

```txt
streamlit
google-cloud-aiplatform
google-cloud-storage
google-cloud-speech
st-audiorec
Pillow
```

---

## Dockerfile

```dockerfile
FROM python:3.11-slim

RUN apt-get update && apt-get install -y     build-essential     curl     software-properties-common     && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

ENV STREAMLIT_SERVER_PORT=8080
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

CMD ["streamlit", "run", "app.py"]
```

---

# 🧩 Step 5: Configure Your App

In `app.py`, update:

```python
PROJECT_ID = "your-project-id"
BUCKET_NAME = "your-bucket-name"
LOCATION = "us-central1"
```

---

# 🎤 Features Included

## ✅ Image Generation (Imagen 4)
- Generate high-quality AI images
- Multiple aspect ratios
- Style presets
- Negative prompts

## ✅ Speech-to-Text
- Record voice
- Convert speech into prompts using Google Speech API

## ✅ Cloud Storage Integration
- Automatically uploads generated images
- Displays saved images in gallery

## ✅ Modern UI
- Styled Streamlit interface
- Sidebar controls
- Asset preview grid

---

# 💻 Step 6: Run Locally

```bash
pip install -r requirements.txt
```

```bash
streamlit run app.py
```

---

# ☁️ Step 7: Deploy to Cloud Run

```bash
gcloud run deploy imagen-studio --source . --region us-central1 --allow-unauthenticated
```

---

# 🧪 How It Works

1. User enters prompt OR records voice
2. Speech is transcribed via Google Speech API
3. Prompt is sent to Imagen 4
4. Images are generated
5. Images are uploaded to Cloud Storage
6. Gallery displays saved images

---

# 📚 Useful Resources

- Vertex AI Docs: https://cloud.google.com/vertex-ai/docs
- Imagen Overview: https://cloud.google.com/vertex-ai/generative-ai/docs/image
- Speech-to-Text Docs: https://cloud.google.com/speech-to-text/docs
- Streamlit Docs: https://docs.streamlit.io
- Cloud Run Docs: https://cloud.google.com/run/docs

---

# ⚠️ Common Issues

## ❌ Permission Errors
Fix:
```bash
gcloud auth application-default login
```

## ❌ API Not Enabled
Enable required APIs again

## ❌ Bucket Not Found
Check bucket name matches exactly

---

# 🧾 Summary

This project demonstrates:

- AI Image Generation (Imagen 4)
- Voice Prompting (Speech-to-Text)
- Cloud Storage Integration
- Full Cloud Deployment Pipeline

---

# 👨‍💻 Author

**Tholumuzi Kuboni**

---

# ⭐ Final Notes

This is a **real-world, production-grade AI application** combining:

- Machine Learning
- Cloud Infrastructure
- Modern UI/UX

Perfect for:
- Developers learning AI
- Startups building tools
- Portfolio projects

---

🔥 Happy Building!
