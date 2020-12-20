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
    with open(USER_CREDS_FILE, "r", encoding="utf8") as file:
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
    with open(USER_CREDS_FILE, "w", encoding="utf8") as file:
        creds_data = {
            "token": user_creds.token,
            "refresh_token": user_creds.refresh_token,
            "token_uri": user_creds.token_uri,
            "client_id": user_creds.client_id,
            "client_secret": user_creds.client_secret,
            "scopes": user_creds.scopes,
        }
        json.dump(creds_data, file)

def get_fileid_from_path(drive_service, doc_path):
    ### Given the path to the Google Doc, finds the id for it
    # Implements method described here: https://stackoverflow.com/a/40998881/4077294

    parts = doc_path.split('/')
    folders, filename = parts[:-1], parts[-1]
    parent_id = None

    # cd thru all the folders
    for folder in folders:
        query = "name = '%s' and mimeType = '%s'" % (folder, "application/vnd.google-apps.folder")
        if parent_id:
            query += " and '%s' in parents" % (parent_id,)
        parent_contents = drive_service.files().list(q=query).execute()
        folder_id = parent_contents['items'][0]['id']
        parent_id = folder_id
    
    # Now look for the file
    query = "name = '%s'" % (filename,)
    if parent_id:
        query += " and '%s' in parents" % (parent_id,)
    parent_contents = drive_service.files().list(q=query).execute()
    return parent_contents['files'][0]['id']

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

    source_id = get_fileid_from_path(drive_service, source)
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
    os.makedirs(os.path.dirname(os.path.abspath(destination)), exist_ok=True)
    with open(destination, 'wb') as f:
        shutil.copyfileobj(fh, f, length=131072)
    
    print(f"Done! Synced {source} with {destination}")
