
# Imagen 4 Studio Pro

![Status](https://img.shields.io/badge/status-production--ready-brightgreen)
![Cloud](https://img.shields.io/badge/cloud-Google%20Cloud-blue)
![AI](https://img.shields.io/badge/AI-Imagen%204-orange)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

A production-ready AI Visual Asset Studio that transforms text and voice into high-quality images using Google Cloud and Imagen 4.

---

## Live Demo

Add your deployed URL here:
```
https://your-cloud-run-url
```

---

## Screenshots

Add screenshots here:

```
/screenshots/home.png
/screenshots/generation.png
/screenshots/gallery.png
```

---

## Demo GIF

Add a short demo recording:

```
/screenshots/demo.gif
```

---

## Features

- Text-to-image generation
- Voice-to-prompt (Speech-to-Text)
- Multi-image generation
- Negative prompting
- Cloud asset storage
- Clean Streamlit UI

---

## Architecture

User → Streamlit → Vertex AI (Imagen 4) → Cloud Storage  
                → Speech-to-Text

---

## Step-by-Step Setup Guide

### 1. Create Google Cloud Project
https://console.cloud.google.com/

---

### 2. Enable APIs

```
gcloud services enable     aiplatform.googleapis.com     run.googleapis.com     cloudbuild.googleapis.com     storage.googleapis.com     speech.googleapis.com
```

---

### 3. Create Storage Bucket

```
gsutil mb -l us-central1 gs://your-unique-bucket-name
```

---

### 4. Clone Repo

```
git clone https://github.com/your-username/imagen4-studio-pro.git
cd imagen4-studio-pro
```

---

### 5. Configure App

Edit `app.py`:

```
PROJECT_ID = "your-project-id"
BUCKET_NAME = "your-bucket-name"
```

---

### 6. Run Locally

```
pip install -r requirements.txt
streamlit run app.py --server.port 8080
```

Open:
http://localhost:8080

---

### 7. Deploy to Cloud Run

```
gcloud run deploy imagen-studio-pro     --source .     --region us-central1     --allow-unauthenticated     --memory 2Gi     --cpu 2
```

---

## Usage Tips

- Use descriptive prompts
- Add styles like "cinematic lighting"
- Use negative prompts for control
- Generate multiple outputs

---

## Portfolio Description (Copy for GitHub)

An enterprise-grade AI Visual Asset Studio that integrates Google Imagen 4, Speech-to-Text, and Cloud Storage into a scalable web application. Built with Streamlit and deployed on Google Cloud Run, this project demonstrates real-world AI product engineering, cloud architecture, and user-focused design.

---

## Tech Stack

- Python
- Streamlit
- Google Vertex AI
- Google Cloud Storage
- Speech-to-Text API
- Docker
- Cloud Run

---

## Folder Structure

```
.
├── app.py
├── requirements.txt
├── Dockerfile
├── screenshots/
└── README.md
```

---

## License

MIT License

---

## Author

Tholumuzi Kuboni
