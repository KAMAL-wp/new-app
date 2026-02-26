# This file handles all Google Drive connection and file operations

import os
import io
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

# This tells Google we only need READ access to Drive (not write/delete)
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def get_drive_service():
    # This function logs into Google Drive and returns a service object
    # The service object is used to make all API calls to Google Drive
    
    creds = None
    
    # Check if we already logged in before (token.json saves the login session)
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If no saved login or login expired, do a fresh login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # Try to refresh the expired login automatically
            creds.refresh(Request())
        else:
            # Open browser window for user to log into Google
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the login session so we don't need to login again next time
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    # Return the Drive service object ready to use
    return build('drive', 'v3', credentials=creds)


def list_files(folder_id):
    # This function lists all files inside a specific Google Drive folder
    # folder_id is the unique ID of the folder from the Drive URL
    
    service = get_drive_service()
    
    # Search for all files in the folder that are not deleted
    results = service.files().list(
        q=f"'{folder_id}' in parents and trashed=false",
        fields="files(id, name, mimeType)"  # Only get id, name and type
    ).execute()
    
    # Return the list of files (empty list if folder is empty)
    return results.get('files', [])


def download_file(file_id, filename):
    # This function downloads a file from Google Drive to our local computer
    # file_id = the unique ID of the file in Drive
    # filename = what to name the file when saved locally
    
    service = get_drive_service()
    
    # Create a download request for the file
    request = service.files().get_media(fileId=file_id)
    
    # Save the file inside a 'downloads' folder
    path = f"downloads/{filename}"
    
    # Create the downloads folder if it doesn't exist
    os.makedirs("downloads", exist_ok=True)
    
    # Download the file in chunks and write to disk
    with open(path, 'wb') as f:
        downloader = MediaIoBaseDownload(f, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()
    
    # Return the local path where file was saved
    return path