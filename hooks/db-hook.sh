#!/usr/bin/env bash

if [[ $1 == "--config" ]] ; then
  cat <<EOF
configVersion: v1
kubernetes:
- apiVersion: k8s.sebatec.eu/v1alpha1
  kind: Database
  executeHookOnEvent: ["Added", "Deleted"]
EOF
else
  for row in $(jq -r '.[] | @base64' $BINDING_CONTEXT_PATH); do
    _jq() {
      echo ${row} | base64 -d | jq -r ${1}
    }
    dbName=$(_jq .object.metadata.name)
    event=$(_jq .watchEvent)

    if [ "${event}" == "Added" ]; then
      mysql -h "127.0.0.1" -u root --password=${MARIADB_ROOT_PASSWORD} -e "CREATE DATABASE IF NOT EXISTS ${dbName}"
    elif [ "${event}" == "Deleted" ]; then
      mysql -h "127.0.0.1" -u root --password=${MARIADB_ROOT_PASSWORD} -e "DROP DATABASE IF EXISTS ${dbName}"
    fi
  done
fi
