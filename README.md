# AI Visual Asset Generator

A professional web application built by Tholumuzi Kuboni. This project demonstrates how to integrate Google Imagen 4 via the Vertex AI API into a functional Streamlit interface, deployed on Google Cloud Platform.

---

## Technical Stack

<p align="left">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/googlecloud/googlecloud-original.svg" alt="Google Cloud" width="40"/>
  <img src="https://www.vectorlogo.zone/logos/docker/docker-icon.svg" alt="Docker" width="40"/>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" alt="Python" width="40"/>
  <img src="https://streamlit.io/images/brand/streamlit-logo-primary-colormark-darktext.png" alt="Streamlit" width="100"/>
</p>

- AI Model: Google Imagen 4 (imagen-4.0-generate-001)  
- Framework: Streamlit (Python)  
- Infrastructure: Google Cloud Vertex AI  
- Deployment: Google Cloud Run & Docker  

---

## Step 1: Initialize the Environment

1. Open the Google Cloud Console: https://console.cloud.google.com/  
2. Click the **Activate Cloud Shell** icon in the top right taskbar.  
3. Enable the required APIs:

```bash
gcloud services enable \
    aiplatform.googleapis.com \
    speech.googleapis.com \
    storage.googleapis.com \
    run.googleapis.com \
    cloudbuild.googleapis.com
```

---

## Step 2: Create the Project Files

Run the following commands in Cloud Shell:

### Create and Enter Directory
```bash
mkdir imaging-app && cd imaging-app
```

### Create Requirements File
```bash
cat <<EOF > requirements.txt
streamlit
google-cloud-aiplatform
google-cloud-storage
google-cloud-speech
st-audiorec
Pillow
numpy
opencv-python-headless
```

### Create Dockerfile
```bash
cat <<EOF > Dockerfile
FROM python:3.11-slim

# Install system dependencies for audio/image processing
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

# Environment variables for Streamlit
ENV STREAMLIT_SERVER_PORT=8080
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

CMD ["streamlit", "run", "app.py"]
```

### Create Application File
```bash
touch app.py
```

---

## Step 3: Create a storage bucket
```bash
# Replace YOUR_BUCKET_NAME with a globally unique bucket name
gcloud storage buckets create gs://YOUR_BUCKET_NAME
```

---

## Step 4: Add the Application Logic

1. Open the Cloud Shell Editor  
2. Navigate to the project folder  
3. Open `app.py`  
4. Paste your application code  
5. Update `PROJECT_ID` with your Google Cloud Project ID
6. Update `BUCKET_NAME` with your Cloud Storage bucket name
7. Save the file  

---

## Step 5: Local Development and Testing

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Streamlit App
```bash
python3 -m streamlit run app.py     --server.port 8080     --server.enableCORS=false     --server.enableXsrfProtection=false     --browser.serverAddress=localhost
```

### Preview Application
Use the **Web Preview** button and select **Preview on port 8080**

---

## Step 6: Deployment to Cloud Run

```bash
gcloud run deploy imaging-app     --source .     --region us-central1     --allow-unauthenticated
```

- Confirm service creation when prompted  
- Retrieve your public Service URL after deployment  

---

## Use Case

This application enables small businesses and creators to generate high-quality marketing visuals without expensive equipment. It simplifies access to advanced AI by providing an intuitive web interface built on scalable cloud infrastructure.

---

## Summary

This project demonstrates a full pipeline:

- Cloud setup  
- Application development  
- Containerization  
- Deployment to production  

You now have a complete, production-ready AI application deployed on a global platform.
