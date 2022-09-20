import os
import pickle

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from base64 import urlsafe_b64decode, urlsafe_b64encode

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from mimetypes import guess_type as guess_mime_type

SCOPES = ['https://www.googleapis.com/auth/gmail.send']
DEFAULT_SUBJECT_LINE = 'Alert!'

class GcpSendMessage(object):

    def __init__(self,
                auth_client_secret,
                from_email,
                to_email,
                subject_line=DEFAULT_SUBJECT_LINE):
        self.auth_client_secret = auth_client_secret
        self.from_email = from_email
        self.to_email = to_email
        self.subject_line = subject_line
        self.services_gmail_api = None

    def authenticate_gmail_api(self):
        creds = None

        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = \
                    InstalledAppFlow.from_client_secrets_file(
                        self.auth_client_secret, SCOPES)
                creds = flow.run_local_server(port=0)

            with open("token.pickle", "wb") as token:
                pickle.dump(creds, token)

        # using Gmail to authenticate
        self.services_gmail_api = build('gmail', 'v1', credentials=creds)

    def add_attachment(self, mail, file_name):
        content_type, encoding = guess_mime_type(file_name)
        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'
        main_type, sub_type = content_type.split('/', 1)
        if main_type == 'text':
            fp = open(file_name, 'rb')
            msg = MIMEText(fp.read().decode(), _subtype=sub_type)
            fp.close()
        elif main_type == 'image':
            fp = open(file_name, 'rb')
            msg = MIMEImage(fp.read(), _subtype=sub_type)
            fp.close()
        elif main_type == 'audio':
            fp = open(file_name, 'rb')
            msg = MIMEAudio(fp.read(), _subtype=sub_type)
            fp.close()
        else:
            fp = open(file_name, 'rb')
            msg = MIMEBase(main_type, sub_type)
            msg.set_payload(fp.read())
            fp.close()

        file_name = os.path.basename(file_name)
        msg.add_header('Content-Disposition', 'attachment', NameofFile=file_name)
        mail.attach(msg)

    def create_mail(self, body, attachments=[]):
        if not attachments:
            mail = MIMEText(body)
            mail['to'] = self.to_email
            mail['from'] = self.from_email
            mail['subject'] = self.subject_line
        else:
            mail = MIMEMultipart()
            mail['to'] = self.to_email
            mail['from'] = self.from_email
            mail['subject'] = self.subject_line
            mail.attach(MIMEText(body))
            for fname in attachments:
                self.add_attachment(mail, fname)

        return {'raw': urlsafe_b64encode(mail.as_bytes()).decode()}

    def send_message(self, body, attachments=[]):
        return self.services_gmail_api.users().messages().send(
                userId="me",
                body=self.create_mail(body, attachments)
            ).execute()
