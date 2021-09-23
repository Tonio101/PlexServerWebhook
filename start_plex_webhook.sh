#!/bin/bash

FLOCK=/usr/bin/flock
LOCK_FILE=/tmp/plexyhook.lockfile
FLOCK_OPTS="-n"

WEBHOOK_SCRIPT=$HOME/PlexServerWebhook/src/plexy_webhook.py
WEBHOOK_ARGS="--config src/plex_webhook_config.local.yml"

$FLOCK $FLOCK_OPTS $LOCK_FILE $WEBHOOK_SCRIPT $WEBHOOK_ARGS
