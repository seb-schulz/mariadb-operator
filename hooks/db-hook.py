#!/usr/bin/env python3

import mysql.connector
import json
import sys
import os

CONFIG = {
    'configVersion':
    'v1',
    'kubernetes': [{
        'apiVersion': 'k8s.sebatec.eu/v1alpha1',
        'kind': 'Database',
        'executeHookOnEvent': ["Added", "Deleted"],
        'jqFilter': ".metadata.name",
    }],
}


def _read_json():
    with open(os.environ['BINDING_CONTEXT_PATH']) as fp:
        return json.load(fp)


def create_database(cur, db_name=None):
    if db_name is None:
        return

    try:
        cur.execute(
            f"CREATE DATABASE IF NOT EXISTS {db_name} DEFAULT CHARACTER SET 'utf8'"
        )
        print(f'{db_name} was added')
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))


def delete_database(cur, db_name=None):
    if db_name is None:
        return

    try:
        cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
        print(f'{db_name} was deleted')
    except mysql.connector.Error as err:
        print("Failed drop database: {}".format(err))


def main():
    conn = mysql.connector.connect(
        user='root',
        password=os.environ['MARIADB_ROOT_PASSWORD'],
        host='127.0.0.1',
    )

    with conn.cursor() as cur:
        for row in _read_json():
            type_ = row.get('type', None)
            watch_ev = row.get('watchEvent', None)

            if type_ == 'Synchronization':
                for obj in row.get('objects', []):
                    create_database(cur, obj.get('filterResult', None))
            elif type_ == 'Event' and watch_ev == 'Added':
                create_database(cur, row.get('filterResult', None))
            elif type_ == 'Event' and watch_ev == 'Deleted':
                delete_database(cur, row.get('filterResult', None))

    conn.close()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--config":
        print(json.dumps(CONFIG))
    else:
        main()
