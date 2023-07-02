import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Authenticate to Google API
gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

# Use credentials to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

def upload_files(drive, parent_folder_id, local_folder_path):
    for filename in os.listdir(local_folder_path):
        path = os.path.join(local_folder_path, filename)
        if os.path.isfile(path):
            print('uploading file: ' + path)
            file_drive = drive.CreateFile({
                'title': filename,
                'parents': [{'id': parent_folder_id}]
            })
            file_drive.SetContentFile(path)
            file_drive.Upload()
            if filename.endswith('.csv') or filename.endswith('.xlsx'):
                print('converting file: ' + filename)
                file_drive.Upload({'convert': True})
        elif os.path.isdir(path):
            print('creating folder: ' + filename)
            folder_drive = drive.CreateFile({
                'title': filename,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [{'id': parent_folder_id}]
            })
            folder_drive.Upload()
            upload_files(drive, folder_drive['id'], path)

# ID of the folder in Google Drive where the files will be uploaded
parent_folder_id = 'your_google_drive_folder_id'

# Local directory that you want to upload
local_folder_path = 'your_local_directory_path'

upload_files(drive, parent_folder_id, local_folder_path)
