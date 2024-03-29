#!/usr/bin/env python3

import argparse
import json
import sys
import yaml

from flask import Flask, request, Response
from model_data import PlexUserEvent
from gcp_send_message import GcpSendMessage

from logger import Logger
log = Logger.getInstance().getLogger()
APP = Flask(__name__)


@APP.route('/webhook', methods=['POST'])
def respond():
    try:
        data = json.loads(request.form.get('payload'))
        log.debug(data)
        log.debug("\n\n\n")

        current_user = PlexUserEvent(data)
        log.info(current_user)
        result = sms.send_message(body=current_user.__str__())
        log.info("Result: {}".format(
            result
        ))

    except Exception as e:
        log.error(e)
        log.error(data)

    return Response(status=200)


def main(argv):
    global sms
    usage = ("{FILE} "
             "--config <config_file.yml> "
             "--debug").format(FILE=__file__)
    description = 'Start plex webhook server'
    parser = argparse.ArgumentParser(usage=usage, description=description)
    parser.add_argument("-c", "--config", help="Config File", required=True)
    parser.add_argument("-d", "--debug", help="Debug", action='store_true',
                        required=False)
    parser.set_defaults(debug=False)
    args = parser.parse_args()

    if args.debug:
        Logger.getInstance().enableDebug()
    Logger.getInstance().enableDebug()

    log.debug(args)

    config = dict()
    with open(args.config, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(2)

    # Deprecated and no longer supported by Google
    # sms = SMSMessage(email=config['SMSInfo']['Email'],
    #                  pas=config['SMSInfo']['Password'],
    #                  sms_gateway=config['SMSInfo']['SMSGateway'],
    #                  smtp_server=config['SMSInfo']['SMTPServer'],
    #                  smtp_port=config['SMSInfo']['SMTPPort'])

    gcp_sms_info = config['GCPSMSInfo']
    sms = GcpSendMessage(
        auth_client_secret=gcp_sms_info['ClientSecretFile'],
        from_email=gcp_sms_info['FromEmail'],
        to_email=gcp_sms_info['ToEmail'],
        subject_line='Plex Server Notification'
    )
    sms.authenticate_gmail_api()

    APP.run(host=config['FlaskApp']['Host'], port=config['FlaskApp']['Port'],
            debug=args.debug)


if __name__ == '__main__':
    main(sys.argv)
