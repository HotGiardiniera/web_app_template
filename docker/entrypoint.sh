#!/bin/bash
set -eou pipefail

ENVIRONMENT=${ENV:-"DEV"}
echo "Starting the server $ENVIRONMENT"
if [ "$ENVIRONMENT" = "LOCAL" ]; then
  python ./database/utils/migrate.py
  echo "Starting development uvicorn server"
  flask --app=main run --host=0.0.0.0 -p 5002
fi
# Infinite loop for debug
while :; do echo "CTRL+C to exit -> ${ENVIRONMENT}"; sleep 1000; done