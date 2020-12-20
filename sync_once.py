import os
import io
import sys
import shutil

import google_auth_oauthlib.flow
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
 
SCOPES = "https://www.googleapis.com/auth/drive.readonly"
DATA_DIR = os.path.expanduser("~/.pdfsync")
CREDS_FILE = "credentials.json"
USER_CREDS_FILE = os.path.join(DATA_DIR, "user_credentials.json")

def load_user_creds():
    ### TODO: Load from USER_CREDS_FILE
    pass

def save_user_creds(user_creds):
    ### TODO: Save to USER_CREDS_FILE
    pass

'''
def get_fileid_from_path(doc_path):
    ### TODO: Given the path to the Google Doc, find the id for it
    pass
'''

def main():
    ### Parse arguments from command line

    if len(sys.argv) < 3:
        print("usage: sync_once <source> <destination>")
        sys.exit(1)
    
    source = sys.argv[1]
    destination = sys.argv[2]

    if not destination.endswith(".pdf"):
        print("destination must be a pdf file")
        sys.exit(1)

    ### Get the credentials
    
    if os.path.isfile(USER_CREDS_FILE):
        user_creds = load_user_creds()
    else:
        flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
        user_creds = flow.run_local_server(port=8080)

        os.makedirs(DATA_DIR, exist_ok=True)
        save_user_creds(user_creds)
    
    ### Build the client
    
    drive_service = build('drive', 'v3', credentials=user_creds)

    ### Use it to export the file

    #source_id = get_fileid_from_path(source)
    source_id = source
    request = drive_service.files().export(fileId=source_id, mimeType='application/pdf')

    # Download the file into memory
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%" % int(status.progress() * 100))

    # Transfer the file from memory to disk
    fh.seek(0)
    os.path.makedirs(os.path.dirname(destination), exist_ok=True)
    with open(destination, 'wb') as f:
        shutil.copyfileobj(fh, f, length=131072)

if __name__ == "__main__":
    main()
