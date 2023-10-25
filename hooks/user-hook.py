#!/usr/bin/env python3

import utils
import hashlib
import os
import hmac
import mysql.connector
import json
from kubernetes import client, config

CONFIG = {
    'configVersion':
    'v1',
    'kubernetes': [{
        'apiVersion': 'k8s.sebatec.eu/v1alpha1',
        'kind': 'User',
        'executeHookOnEvent': ["Added", "Modified", "Deleted"],
    }],
}


def delete_user(cur, name=None):
    if name is None:
        return

    try:
        sql = f"DROP USER IF EXISTS '{name}'"
        cur.execute(sql)
        print(f'{name} was deleted')
    except mysql.connector.Error as err:
        print("Failed drop database: {}".format(err))


def create_user(cur, name=None, passwd=None):
    if name is None:
        return

    try:
        sql = f"CREATE USER IF NOT EXISTS '{name}'@'%' IDENTIFIED BY '{passwd}'"
        cur.execute(sql)
        print(f'{name} was added')
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))


def set_password(cur, name=None, passwd=None):
    if name is None:
        return

    try:
        sql = f"SET PASSWORD FOR '{name}'@'%' = PASSWORD('{passwd}');"
        cur.execute(sql)
        print(f'{name} password was modified')
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))


def revoke_all_permission(cur, user=None):
    if user is None:
        return

    try:
        sql = f"REVOKE IF EXISTS ALL PRIVILEGES, GRANT OPTION FROM '{user}'@'%'; FLUSH PRIVILEGES;"
        cur.execute(sql, multi=True)
        print(f'Database permission for {user} revoked')
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))


def grant_database_permission(cur, user=None, db=None):
    if user is None or db is None:
        return

    try:
        sql = f"GRANT ALL PRIVILEGES ON `{db}`.* TO '{user}'@'%'; FLUSH PRIVILEGES;"
        cur.execute(sql, multi=True)
        print(f'Database permission on {db} for {user} given')
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))


def get_user(obj):
    return obj.get('metadata', {}).get('name', None)


def get_db(obj):
    return obj.get('spec', {}).get('database', None)


def get_passwd(obj):
    SALT = 'users.k8s.sebatec.eu'
    ITER = 500_000
    user = get_user(obj)
    site_name = obj.get('data', {}).get('derivedPassword', {}).get(
        'siteName',
        obj.get('metadata', {}).get('namespace', 'default'),
    )
    site_counter = obj.get('data', {}).get('derivedPassword', {}).get(
        'siteCounter',
        1,
    )

    mKey = hashlib.pbkdf2_hmac(
        'sha256',
        os.environ['MARIADB_OPERATOR_SEED'].encode('utf-8'),
        '{}{}{}'.format(SALT, len(user), user).encode('utf-8'),
        ITER,
        64,
    )

    return hmac.HMAC(
        mKey,
        '{}{}{}{}'.format(
            SALT,
            len(site_name),
            site_name,
            site_counter,
        ).encode('utf-8'),
        digestmod=hashlib.sha256,
    ).hexdigest()


def create_or_replace_config_map(name, namespace, user):
    cmap = client.V1ConfigMap()
    cmap.metadata = client.V1ObjectMeta(name=name)
    cmap.data = {}
    cmap.data['MARIADB_SERVICE_PORT'] = os.environ['MARIADB_SERVICE_PORT']
    cmap.data['MARIADB_SERVICE_DOMAIN'] = os.environ['MARIADB_SERVICE_DOMAIN']
    cmap.data['MARIADB_USER'] = user

    api_instance = client.CoreV1Api()
    try:
        api_instance.replace_namespaced_config_map(name=name,
                                                   namespace=namespace,
                                                   body=cmap)
    except client.exceptions.ApiException as e:
        if e.status == 404:
            api_instance.create_namespaced_config_map(namespace=namespace,
                                                      body=cmap)
        else:
            print(f"failed to create config: {e!r}")


def delete_config_map(name, namespace):
    api_instance = client.CoreV1Api()
    try:
        api_instance.delete_namespaced_config_map(name, namespace)
    except client.exceptions.ApiException as e:
        if e.status != 404:
            print(f"failed to create config: {e!r}")


def handle_sync(cur, objects):
    for item in objects:
        obj = item.get('object', {})
        create_user(cur, get_user(obj), get_passwd(obj))
        db = get_db(obj)
        if db is not None:
            grant_database_permission(cur, get_user(obj), get_db(obj))
            for cm in obj.get('spec', {}).get('configMaps'):
                create_or_replace_config_map(
                    cm.get('name'),
                    cm.get(
                        'namespace',
                        obj.get('metadata', {}).get('namespace', 'default'),
                    ), get_user(obj))


def handle_event(cur, watch_ev, obj):
    if watch_ev == 'Deleted':
        old_obj = json.loads(
            obj.get('metadata', {}).get(
                'annotations',
                {},
            ).get('kubectl.kubernetes.io/last-applied-configuration', ""))

        delete_user(cur, get_user(old_obj))
        for cm in old_obj.get('spec', {}).get('configMaps', []):
            delete_config_map(
                cm.get('name'),
                cm.get(
                    'namespace',
                    obj.get('metadata', {}).get('namespace', 'default'),
                ),
            )
    elif watch_ev == 'Added':
        create_user(cur, get_user(obj), get_passwd(obj))
        grant_database_permission(cur, get_user(obj), get_db(obj))
        for cm in obj.get('spec', {}).get('configMaps', []):
            create_or_replace_config_map(
                cm.get('name'),
                cm.get(
                    'namespace',
                    obj.get('metadata', {}).get('namespace', 'default'),
                ),
                get_user(obj),
            )
    elif watch_ev == 'Modified':
        set_password(cur, get_user(obj), get_passwd(obj))

        db, user = get_db(obj), get_user(obj)
        if db is None:
            revoke_all_permission(cur, user)
        else:
            grant_database_permission(cur, user, db)

        for cm in obj.get('spec', {}).get('configMaps', []):
            create_or_replace_config_map(
                cm.get('name'),
                cm.get(
                    'namespace',
                    obj.get('metadata', {}).get('namespace', 'default'),
                ),
                get_user(obj),
            )
    else:
        print(f'Cannot handle watchEvent {watch_ev!r}')


def main():
    config.load_incluster_config()
    with utils.db_cursor() as cur:
        for row in utils.read_binding_context():
            type_ = row.get('type', None)
            if type_ == 'Synchronization':
                handle_sync(cur, row.get('objects', []))
            elif type_ == 'Event':
                handle_event(cur, row.get('watchEvent', None),
                             row.get('object', {}))


if __name__ == "__main__":
    utils.main_runner(CONFIG, main)
