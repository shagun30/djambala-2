#!/bin/sh

PYTHON="/usr/bin/python"
CURRENT_DIR="../../"
PYTHONPATH="$CURRENT_DIR"
DJANGO_SETTINGS_MODULE="dms.settings"
export PYTHONPATH DJANGO_SETTINGS_MODULE

exec "$PYTHON" delete_old_resevents.py
