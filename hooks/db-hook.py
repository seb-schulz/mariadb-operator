#!/usr/bin/env python3

import mysql.connector
import sys
import os
import utils

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
    with utils.db_cursor() as cur:
        for row in utils.read_binding_context():
            type_ = row.get('type', None)
            watch_ev = row.get('watchEvent', None)

            if type_ == 'Synchronization':
                for obj in row.get('objects', []):
                    create_database(cur, obj.get('filterResult', None))
            elif type_ == 'Event' and watch_ev == 'Added':
                create_database(cur, row.get('filterResult', None))
            elif type_ == 'Event' and watch_ev == 'Deleted':
                delete_database(cur, row.get('filterResult', None))


if __name__ == "__main__":
    utils.main_runner(CONFIG, main)
