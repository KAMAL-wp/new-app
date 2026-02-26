# Document Summarizer via Google Drive

## What it does
This app connects to Google Drive, reads documents (PDF, DOCX, TXT), 
and uses AI to summarize each document. Results are shown on a web page 
with a downloadable CSV report.

## Tech Stack
- Python & Flask (web server)
- Google Drive API (document access)
- Groq AI / LLaMA3 (summarization)
- PyMuPDF, python-docx (document parsing)

## Setup Steps

### 1. Clone the repository
git clone <your-github-link>
cd app

### 2. Install dependencies
python -m pip install flask google-auth google-auth-oauthlib google-api-python-client PyMuPDF python-docx pdfplumber groq

### 3. Add credentials.json
Download OAuth credentials from Google Cloud Console and save as credentials.json

### 4. Add your API keys
- Add Groq API key in summarizer.py
- Add Google Drive Folder ID in app.py

### 5. Run the app
python app.py

### 6. Open browser
Go to http://127.0.0.1:5000