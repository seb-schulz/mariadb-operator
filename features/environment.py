from contextlib import contextmanager
import mysql.connector
import os
from behave.runner import Context
import subprocess


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
    context.cleanup_users = []
    context.cleanup_namespaces = []
    context.cleanup_k8s_configs = []


def after_scenario(context, scenario):
    if 'shell_operator' in context:
        context.shell_operator.terminate()

    with context.db_cursor() as cur:
        for db in context.cleanup_databases:
            cur.execute(f"DROP DATABASE IF EXISTS {db}")

        for user in context.cleanup_users:
            cur.execute(f"DROP USER IF EXISTS '{user}'")

    for ns in context.cleanup_namespaces:
        subprocess.run(['kubectl', 'delete', 'namespace', '--now', '--ignore-not-found', ns])

    for config in context.cleanup_k8s_configs:
        subprocess.run(['kubectl', 'delete', '--now', '--ignore-not-found', '-f', '-'], text=True, input=config, capture_output=True)
