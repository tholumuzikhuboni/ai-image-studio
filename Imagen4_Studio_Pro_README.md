# Imagen 4 Studio Pro: AI Visual Asset Generator

Imagen 4 Studio Pro is a professional, enterprise-grade web application designed to generate high-quality visual assets using artificial intelligence. The platform integrates Google Cloud services, advanced AI models, and an intuitive user interface to provide a seamless creative workflow.

This project was built by Tholumuzi Kuboni and demonstrates how modern AI tools can be combined into a production-ready system.

---

## Overview

Imagen 4 Studio Pro transforms simple text or voice inputs into visually rich images. It is designed for developers, designers, and creative teams who want to quickly generate, manage, and store visual assets in a scalable cloud environment.

---

## Technical Stack

### Core Technologies

- Google Vertex AI (Imagen 4 model) for image generation
- Google Cloud Speech-to-Text for voice input processing
- Google Cloud Storage for persistent asset storage
- Streamlit for building the web interface
- Docker for containerization
- Google Cloud Run for deployment and scalability
- Python as the primary programming language

---

## Features

### Voice-to-Prompt
Users can speak their ideas instead of typing. The application converts speech into text using Google Cloud Speech-to-Text, which is then used as an image prompt.

### Multi-Image Generation
Generate multiple image variations (up to four) at the same time to explore different creative outputs quickly.

### Negative Prompting
Control the output more precisely by specifying elements you want to exclude, such as "blurry", "low quality", or "text".

### Asset Library
Every generated image is automatically stored in a Google Cloud Storage bucket. This creates a persistent and organized gallery of assets.

### Studio Interface
A clean, dark-themed interface designed for professional use, allowing users to focus on creativity without distractions.

---

## Getting Started

### Step 1: Set Up Google Cloud

1. Open the Google Cloud Console
2. Launch Cloud Shell
3. Enable required services:

```
gcloud services enable \
    aiplatform.googleapis.com \
    run.googleapis.com \
    cloudbuild.googleapis.com \
    storage.googleapis.com \
    speech.googleapis.com
```

4. Create a storage bucket:

```
gsutil mb -l us-central1 gs://your-unique-bucket-name
```

Replace "your-unique-bucket-name" with your own globally unique name.

---

### Step 2: Configure the Application

Open the `app.py` file and update the following variables:

- PROJECT_ID: Your Google Cloud project ID
- BUCKET_NAME: The name of your storage bucket

---

### Step 3: Run Locally

Install dependencies:

```
pip install -r requirements.txt
```

Start the application:

```
streamlit run app.py --server.port 8080
```

Then open your browser and go to:

http://localhost:8080

---

### Step 4: Deploy to Cloud Run

Deploy the application using:

```
gcloud run deploy imagen-studio-pro \
    --source . \
    --region us-central1 \
    --allow-unauthenticated \
    --memory 2Gi \
    --cpu 2
```

After deployment, Google Cloud will provide a public URL to access your application.

---

## How It Works

1. The user provides a prompt (text or voice)
2. The prompt is processed and sent to the Imagen 4 model
3. The model generates one or more images
4. Images are stored in Google Cloud Storage
5. The application displays the results in a gallery interface

---

## Use Case: Creative Teams

This platform is especially useful for:

- Marketing teams generating campaign visuals
- Designers exploring rapid prototypes
- Content creators building social media assets
- Businesses maintaining a centralized asset library

---

## Project Structure (Simplified)

- app.py: Main Streamlit application
- requirements.txt: Python dependencies
- Dockerfile: Container configuration
- README.md: Project documentation

---

## Best Practices

- Use clear and descriptive prompts for better results
- Experiment with negative prompts to refine outputs
- Organize your storage bucket with folders if scaling usage
- Monitor Cloud costs when using AI and storage services

---

## License and Credits

This project was developed by Tholumuzi Kuboni.

It is powered by Google Cloud technologies, including Vertex AI and the Imagen 4 model.
