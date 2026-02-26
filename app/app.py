# This is the main Flask application file
# It connects all the pieces together and runs the web server

from flask import Flask, render_template, request
from drive_helper import list_files, download_file
from parser_helper import extract_text
from summarizer import summarize
from report_generator import generate_csv

# Create the Flask app
app = Flask(__name__)

# Paste your Google Drive folder ID here
# To find it: open your Drive folder in browser, copy the ID from the URL
# Example URL: drive.google.com/drive/folders/1A2B3C4D5E  <- this part is the ID
FOLDER_ID = "1hjDkAPaXXs08-_BpmnGx_CR2mK51I355"

@app.route('/')
def index():
    # This is the home page route
    # When user visits the website, show the index.html page
    return render_template('index.html', summaries=None)

@app.route('/summarize', methods=['POST'])
def run_summarizer():
    # This route runs when user clicks the Summarize button
    # It downloads files from Drive, extracts text and summarizes them
    
    # Get list of all files in the Google Drive folder
    files = list_files(FOLDER_ID)
    
    # Empty list to store all summaries
    summaries = []

    for file in files:
        name = file['name']
        
        # Only process PDF, DOCX and TXT files
        # Skip any other file types like images or videos
        if not any(name.endswith(ext) for ext in ['.pdf', '.docx', '.txt']):
            print(f"Skipping unsupported file: {name}")
            continue
        
        print(f"Processing: {name}")
        
        # Download the file from Google Drive to local downloads folder
        path = download_file(file['id'], name)
        
        # Extract text content from the downloaded file
        text = extract_text(path)
        
        # Send text to Gemini AI and get summary back
        summary = summarize(text, name)
        
        # Add the filename and summary to our list
        summaries.append({"filename": name, "summary": summary})
        
        print(f"Done: {name}")

    # Generate a downloadable CSV report with all summaries
    generate_csv(summaries)
    
    # Show the results on the web page
    return render_template('index.html', summaries=summaries)

if __name__ == '__main__':
    # Start the Flask web server in debug mode
    # Debug mode shows errors clearly during development
    app.run(debug=True)