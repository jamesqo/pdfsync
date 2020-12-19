import os
import io
import sys
import shutil

import google_auth_oauthlib.flow
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
 
class Auth:
    def __init__(self, client_secret_filename, user_creds_filename, scopes):
        self.client_secret = client_secret_filename
        self.user_creds = user_creds_filename
        self.scopes = scopes
        self.flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(self.client_secret, self.scopes)
        self.flow.redirect_uri = 'http://localhost:8080/'
        self.creds = None
 
    def get_credentials(self):
        if os.path.isfile(self.user_creds):
            return self.load_user_creds_from_json()

        flow = InstalledAppFlow.from_client_secrets_file(self.client_secret, self.scopes)
        self.creds = flow.run_local_server(port=8080)
        self.save_user_creds_to_json(self.creds)
        return self.creds

    def load_user_creds_from_json(self):
        pass # TODO

    def save_user_creds_to_json(self, creds):
        os.makedirs(os.path.dirname(self.user_creds), exist_ok=True)
        
### Build the client

SCOPES = "https://www.googleapis.com/auth/drive.readonly"
DATA_DIR = os.path.expanduser("~/.pdfsync")
CLIENT_SECRET_FILE = "credentials.json"
USER_CREDS_FILE = os.path.join(DATA_DIR, "user_credentials.json")

credentials = Auth(
    client_secret_filename=CLIENT_SECRET_FILE,
    user_creds_filename=USER_CREDS_FILE,
    scopes=SCOPES
).get_credentials()
 
drive_service = build('drive', 'v3', credentials=credentials)

### Use it to export the file

request = drive_service.files().export(fileId='1msTothwvq8dXCsV6cmhaZhYNQiYu6zWT1aLG5iUF_HI', mimeType='application/pdf')

fh = io.BytesIO()
downloader = MediaIoBaseDownload(fh, request)
done = False
while done is False:
    status, done = downloader.next_chunk()
    print("Download %d%%" % int(status.progress() * 100))

# The file has been downloaded into RAM, now save it in a file
fh.seek(0)
with open('your_filename.pdf', 'wb') as f:
    shutil.copyfileobj(fh, f, length=131072)
