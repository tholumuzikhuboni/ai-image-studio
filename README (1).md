# AI Image Generator and Editor (Google Cloud + Imagen)

This guide is written for beginners. Follow each step carefully.

-----------------------------------

STEP 1: Create a Google Cloud Account

Go to:
https://console.cloud.google.com/

Create an account and start the free trial.

Note:
Google Cloud may charge you depending on usage. Always monitor billing.

-----------------------------------

STEP 2: Create a Project

1. Click "Select Project"
2. Click "New Project"
3. Enter a name
4. Click Create

-----------------------------------

STEP 3: Open Cloud Shell

Click the terminal icon in the top right.

-----------------------------------

STEP 4: Enable APIs

Run:

gcloud services enable aiplatform.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable storage.googleapis.com

-----------------------------------

STEP 5: Create Project Files

Create folder:

mkdir imagen-app
cd imagen-app

Create app.py:

cat <<EOF > app.py
PASTE YOUR APP CODE HERE
EOF

Create requirements.txt:

cat <<EOF > requirements.txt
streamlit
google-cloud-aiplatform
google-cloud-storage
Pillow
EOF

Create Dockerfile:

cat <<EOF > Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8080
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
EOF

-----------------------------------

STEP 6: Update Configuration

In app.py:

PROJECT_ID = "your-project-id"
BUCKET_NAME = "your-bucket-name"

-----------------------------------

STEP 7: Run Locally

pip install -r requirements.txt

streamlit run app.py

-----------------------------------

STEP 8: Deploy

gcloud run deploy imagen-app --source . --region us-central1 --allow-unauthenticated

-----------------------------------

FEATURES

- Generate images using Imagen
- Upload image and modify it using prompts
- Save images to Cloud Storage

-----------------------------------

COMMON ERRORS

Permission error:
gcloud auth application-default login

-----------------------------------

END
