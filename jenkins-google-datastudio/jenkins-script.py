import jenkinsapi
import google.auth
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Load the credentials from the JSON file
creds = Credentials.from_service_account_file('$credential.json')

# Authenticate with Google Drive API
drive_service = build('drive', 'v3', credentials=creds)

# Connect to Jenkins instance
J = jenkinsapi.jenkins.Jenkins('$<<<jenkins-cloud-url>>>:8080', username='$user-name', password='$password')

# Get the latest build artifacts from Jenkins
last_build = J.get_job('jenkins-gdrive').get_last_build()
artifacts = last_build.get_artifacts()

# Upload each artifact to Google Drive
for artifact in artifacts:
    file_metadata = {'name': artifact.filename}
    media = artifact.get_data()
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print('File'{Result.xlsx}' has been uploaded to Google Drive with ID:'{file.get("[[[REDACTED]]]")})
