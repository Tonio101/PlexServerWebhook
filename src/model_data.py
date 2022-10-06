import smtplib

from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from smtplib import SMTPServerDisconnected, SMTPNotSupportedError,\
                    SMTPSenderRefused
from logger import Logger
log = Logger.getInstance().getLogger()


class PlexUserEvent(object):

    def __init__(self, data):
        self.event = data['event']
        self.name = data['Account']['title']
        self.server = data['Server']['title']
        self.player = data['Player']['title']
        self.publicIpv4Addr = data['Player']['publicAddress']
        self.type = data['Metadata']['type']
        self.title = data['Metadata']['title']

    def __str__(self) -> str:
        curr_ts = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        to_str = ("Event: {EVENT}\nName: {NAME}\n"
                  "Server: {SERVER}\nPlayer: {PLAYER}\n"
                  "Type: {TYPE}\nTitle: {TITLE}\n"
                  "IP Address: {IP}\n{TS}\n").format(
                      EVENT=self.event,
                      NAME=self.name,
                      SERVER=self.server,
                      PLAYER=self.player,
                      TYPE=self.type,
                      TITLE=self.title,
                      IP=self.publicIpv4Addr,
                      TS=curr_ts
                  )
        return to_str


class SMSMessage(object):

    def __init__(self, email, pas, sms_gateway,
                 smtp_server='smtp.gmail.com', smtp_port=587):
        self.email = email
        self.pas = pas
        self.sms_gateway = sms_gateway
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.start_email_server()

    def send_message(self, subject='', body=''):
        msg = MIMEMultipart()
        msg['From'] = self.email
        msg['To'] = self.sms_gateway
        msg['Subject'] = 'Plex Server Notification\n'
        msg.attach(MIMEText(body, 'plain'))
        sms = msg.as_string()

        try:
            self.server.sendmail(self.email, self.sms_gateway, sms)
            log.info("Notification sent")
        except (SMTPServerDisconnected, SMTPNotSupportedError,
                SMTPSenderRefused):
            log.info("SMTP server is disconnected, reconnect...")
            # self.server.starttls()
            # self.server.login(self.email, self.pas)
            self.start_email_server()
            self.server.sendmail(self.email, self.sms_gateway, sms)
            log.info("Notification sent")

    def start_email_server(self):
        # Start email server
        self.server = smtplib.SMTP(self.smtp_server,
                                   self.smtp_port)
        self.server.starttls()
        # TODO - Error check to make sure server started.
        self.server.login(self.email, self.pas)

    def kill_email_server(self):
        self.server.quit()
