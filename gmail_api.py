import os
import sys
import time
import re
import json

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import os, requests, socks, socket
socks.set_default_proxy()
socket.socket = socks.socksocket


dir_name = os.path.dirname(os.path.abspath(__file__)) + os.sep
os.chdir(dir_name)

SCOPES = ['https://mail.google.com/']

def gmail_authenticate(userId):
    creds = None
    # the file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time
    token_file = f'token_{userId}.json'
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    # if there are no (valid) credentials availablle, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=36666)
        # save the credentials for the next run
        with open(token_file, "w") as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)


def search_messages(service, query):
    result = service.users().messages().list(userId='me',q=query).execute()
    messages = []
    if 'messages' in result:
        messages.extend(result['messages'])
    while 'nextPageToken' in result:
        page_token = result['nextPageToken']
        result = service.users().messages().list(userId='me',q=query, pageToken=page_token).execute()
        if 'messages' in result:
            messages.extend(result['messages'])
    return messages


if __name__ == "__main__":
    email = sys.argv[1:]
    for userId in email:
        service = gmail_authenticate(userId)
    
