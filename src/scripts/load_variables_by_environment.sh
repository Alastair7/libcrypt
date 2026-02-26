#!/bin/bash

if [ $# -eq 0 ]; then
   echo "Missing argument: env is required to load"
   exit 1
fi

env=${1,,}

case "$env" in 
   dev|np|prod)
      ;;
   *)
      echo "Error: Invalid environment '$env'. Must be: dev,np or prod."
      exit 1
      ;;
esac

SCRIPT_DIR=$(dirname "$(realpath "$0")")
APP_CONFIG="$SCRIPT_DIR/../../appconfig.yml"

while IFS='=' read -r key value; do
   echo "$key=$value"
done < <(
   yq ".app.environment_variables.$env | to_entries | .[] | \"\(.key)=\(.value)\"" "$APP_CONFIG"
)

exit 0
