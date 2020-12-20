import io
import json
import os
import shutil
import sys

import google_auth_oauthlib.flow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
 
SCOPES = "https://www.googleapis.com/auth/drive.readonly"
DATA_DIR = os.path.expanduser("~/.pdfsync")
CREDS_FILE = "credentials.json"
USER_CREDS_FILE = os.path.join(DATA_DIR, "user_credentials.json")

def load_user_creds():
    with open(USER_CREDS_FILE, "rb", encoding="utf8") as file:
        creds_data = json.load(file)
        cred = Credentials(
            token=creds_data['token'],
            refresh_token=creds_data['refresh_token'],
            token_uri=creds_data['token_uri'],
            client_id=creds_data['client_id'],
            client_secret=creds_data['client_secret'],
            scopes=creds_data['scopes']
        )
    return cred

def save_user_creds(user_creds):
    with open(USER_CREDS_FILE, "rw", encoding="utf8") as file:
        creds_data = {
            "token": user_creds.token,
            "refresh_token": user_creds.refresh_token,
            "token_uri": user_creds.token_uri,
            "client_id": user_creds.client_id,
            "client_secret": user_creds.client_secret,
            "scopes": user_creds.scopes,
        }
        json.dump(creds_data, file)

'''
def get_fileid_from_path(doc_path):
    ### TODO: Given the path to the Google Doc, find the id for it
    pass
'''

def sync_once(source, destination):
    if not destination.endswith(".pdf"):
        raise Exception("destination must be a pdf file")

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
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    with open(destination, 'wb') as f:
        shutil.copyfileobj(fh, f, length=131072)
