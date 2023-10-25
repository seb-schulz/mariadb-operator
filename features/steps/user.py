from behave import *
import subprocess
import time
import json


@then(u'user "{user}" exists')
def step_impl(context, user):
    context.cleanup_users.append(user)
    with context.db_cursor() as cur:
        for i in range(3):
            cur.execute("SELECT 1 FROM mysql.user WHERE User = %s;", [user])
            r = cur.fetchone()
            if r is not None:
                assert r[0], "user does not exist"
                break
            time.sleep(0.25)


@then(u'user "{user}" does not exist')
def step_impl(context, user):
    context.cleanup_users.append(user)
    with context.db_cursor() as cur:
        for i in range(3):
            cur.execute("SELECT 1 FROM mysql.user WHERE User = %s;", [user])
            r = cur.fetchone()
            if r is None:
                break
            time.sleep(0.25)
            assert r is None, "user exists"


@when(u'namespace "{namespace}" exists')
def step_impl(context, namespace):
    context.cleanup_namespaces.append(namespace)
    r = subprocess.run(['kubectl', 'create', 'namespace', namespace],
                       text=True,
                       capture_output=True)
    assert r.returncode == 0, f'failed to create namespace: {r!r}'


@then(u'secret "{name}" does exist in namespace "{ns}" with following entries')
def step_impl(context, name, ns):
    for i in range(3):
        time.sleep(i + 1)
        r = subprocess.run([
            'kubectl', 'get', 'secret', '-n', ns, name,
            r"-o=jsonpath='{.data}'"
        ],
                           text=True,
                           capture_output=True)
        if r.returncode == 0:
            break
    assert r.returncode == 0, "secret was not created"
    assert len(r.stdout) > 2, f'secret has no data: {r!r}'
    cm = json.loads(r.stdout[1:-1])
    for row in context.table:
        k = row['key']
        assert k in cm.keys(), f"key {k} does not exist in secret"


@then(
    u'config map "{name}" does exist in namespace "{ns}" with following entries'
)
def step_impl(context, name, ns):
    for i in range(3):
        time.sleep(i + 1)
        r = subprocess.run(
            ['kubectl', 'get', 'cm', '-n', ns, name, r"-o=jsonpath='{.data}'"],
            text=True,
            capture_output=True)
        if r.returncode == 0:
            break
    assert r.returncode == 0, "config map was not created"
    assert len(r.stdout) > 2, f'config map has no data: {r!r}'
    cm = json.loads(r.stdout[1:-1])
    for row in context.table:
        k = row['key']
        assert k in cm.keys(), f"key {k} does not exist in config map"
        assert cm[k] == row[
            'value'], f"\"{cm[k]}\" are \"{row['value']}\" not equal"
