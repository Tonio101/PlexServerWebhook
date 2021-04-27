#!/bin/bash

FLOCK=/usr/bin/flock
LOCK_FILE=/tmp/plex_webhook.lockfile
FLOCK_OPTS="-n"

WEBHOOK_SCRIPT=$HOME/DEV/PlexServerWebhook/src/plex_webhook.py
WEBHOOK_ARGS="--phone <phone_number>"

$FLOCK $FLOCK_OPTS $LOCK_FILE $WEBHOOK_SCRIPT $WEBHOOK_ARGS
