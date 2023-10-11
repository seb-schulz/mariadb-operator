import os
import json
import sys
import mysql.connector

from contextlib import contextmanager


def read_binding_context():
    with open(os.environ['BINDING_CONTEXT_PATH']) as fp:
        return json.load(fp)


def main_runner(config, main_fn):
    if len(sys.argv) > 1 and sys.argv[1] == "--config":
        print(json.dumps(config))
    else:
        main_fn()
    sys.exit(0)


@contextmanager
def db_cursor():
    conn = mysql.connector.connect(
        user='root',
        password=os.environ['MARIADB_ROOT_PASSWORD'],
        host='127.0.0.1',
    )

    try:
        with conn.cursor() as cur:
            yield cur
    finally:
        conn.close()
