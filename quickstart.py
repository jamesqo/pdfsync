import google_auth_oauthlib.flow
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io
import sys
import shutil
 
class Auth:
    def __init__(self, client_secret_filename, scopes):
        self.client_secret = client_secret_filename
        self.scopes = scopes
        self.flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(self.client_secret, self.scopes)
        self.flow.redirect_uri = 'http://localhost:8080/'
        self.creds = None
 
    def get_credentials(self):
        flow = InstalledAppFlow.from_client_secrets_file(self.client_secret, self.scopes)
        self.creds = flow.run_local_server(port=8080)
        return self.creds

 
# The scope you app will use. 
# (NEEDS to be among the enabled in your OAuth consent screen)
SCOPES = "https://www.googleapis.com/auth/drive.readonly"
CLIENT_SECRET_FILE = "credentials.json"
 
credentials = Auth(client_secret_filename=CLIENT_SECRET_FILE, scopes=SCOPES).get_credentials()
 
drive_service = build('drive', 'v3', credentials=credentials)

'''
print('hi')

request = drive_service.files().list().execute()
print(request)

print('hello world')

sys.exit(1)
'''

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
