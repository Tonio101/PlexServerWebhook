import argparse
import json
import logging
import re
import sys
import time

from logging.handlers import RotatingFileHandler
from flask import Flask, request, Response
from model_data import PlexUser
from subprocess import PIPE, Popen

APP     = Flask(__name__)
APP_DBG = False

HOST    = '0.0.0.0'
PORT    = 6669

LOG_FILE            = '/tmp/plex_webhook.log'
LOG_FILE_MAXSIZE    = 10 * 1024 * 1024 # 10MB
LOG_FILE_BACKUP_CNT = 3

PHONE_NUMBER        = '1234567890'

logging.basicConfig(filename=LOG_FILE, level=logging.INFO)
logger = logging.getLogger(__file__)

def cmd_line(command):
    """
    Helper function to run CLI command.
    :param command: Command to run.
    :return: output
    """
    process = Popen(args=command,
                    stdout=PIPE,
                    shell=True)
    return process.communicate()[0]

def config_logger():
    """
    Configure logger
    """
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s:%(levelname)s - %(message)s',
            "%Y-%m-%d %H:%M:%S")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    rotate_file_handler = RotatingFileHandler(LOG_FILE,
            maxBytes=LOG_FILE_MAXSIZE, backupCount=LOG_FILE_BACKUP_CNT)
    logger.addHandler(rotate_file_handler)


def init():
    config_logger()

    usage = '{FILE} --phone 1234567890 --host 0.0.0.0 --port 6669'.format(FILE=__file__)
    description = 'Start webhook server for Plex and notifiy user via text message'
    parser = argparse.ArgumentParser(usage=usage, description=description)
    parser.add_argument("-p", "--phone", help="Phone number (T-Mobile only for now)", required=True)
    parser.add_argument("--host", help="Webhook server IP", required=False)
    parser.add_argument("--port", help="Webhook server port", required=False)
    args = parser.parse_args()

    pattern = re.compile('^[0-9]{10}$')
    if not pattern.match(args.phone):
        logger.info("Invalid phone number, example: 1234567890")
        sys.exit(2)

    global PHONE_NUMBER
    PHONE_NUMBER = args.phone

@APP.route('/webhook', methods=['POST'])
def respond():
    """
    Handle POST request sent from Plex server
    """
    #curl -kv -X POST -H "Content-Type: application/json" \
    #        -d '{"username": "test", "content": "hello"}' \
    #        "https://<SERVER_IP>:6669/webhook"
    #print(request.json)

    data = json.loads(request.form.get('payload'))
    logger.debug(data)

    current_user = PlexUser(event=data['event'],
                            user=data['Account']['title'],
                            server=data['Server']['title'],
                            player=data['Player'],
                            type=data['Metadata']['type'],
                            title=data['Metadata']['title'])
    message = "Event:{0}\nUser:{1}\nTitle:{2}\nIP:{3}\nPlayer:{4}"

    message = message.format(current_user.event, current_user.user, current_user.title,
            current_user.player['publicAddress'], current_user.player['title'])
    cmd_str = "echo \"{MSG}\" | mail -s 'Plex Server Webhook' {PHONE}@tmomail.net".format(
            MSG=message, PHONE=PHONE_NUMBER)
    logger.debug(cmd_str)
    cmd_line(cmd_str)

    return Response(status=200)

def main(argv):
    init()
    APP.run(host=HOST, port=PORT, debug=APP_DBG)

if __name__ == '__main__':
    main(sys.argv)
