from contextlib import contextmanager
import mysql.connector
import os
from behave.runner import Context


@contextmanager
def _db_cursor():
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

def before_all(context:Context):
    context.db_cursor = _db_cursor

def before_scenario(context:Context, scenario):
    context.cleanup_databases = []

def after_scenario(context, scenario):
    if 'shell_operator' in context:
        context.shell_operator.terminate()

    with context.db_cursor() as cur:
        for db in context.cleanup_databases:
            cur.execute(f"DROP DATABASE IF EXISTS {db}")
