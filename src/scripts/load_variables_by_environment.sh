#!/bin/bash

# This script exports into PATH the environment variables of appconfig.yaml

if [ $# -eq 0 ]; then
   echo "Missing argument: env is required to load"
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

while IFS='=' read -r key value; do
   export "$key=$value"
done < <(
   yq '.app.environment_variables.dev | to_entries | .[] | "\(.key)=\(.value)"' ../../appconfig.yml
)
