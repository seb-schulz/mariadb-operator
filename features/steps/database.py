from behave import *
import subprocess
import time

@given(u'a running shell-operator')
def step_impl(context):
    context.shell_operator = subprocess.Popen(["/shell-operator", 'start'], stderr=subprocess.PIPE)
    time.sleep(1)


@when(u'following kubernetes configuration is applied')
def step_impl(context):
    r = subprocess.run(['kubectl', 'apply', '-f', '-'], text=True, input=context.text, capture_output=True)
    assert r.returncode == 0, f'failed to apply resource: {r!r}'
    context.previous_text = context.text

@when(u'previous kubernetes configuration is deleted')
def step_impl(context):
    assert 'previous_text' in context, 'no configuration from previous steps'

    r = subprocess.run(['kubectl', 'delete', '-f', '-'], text=True, input=context.previous_text, capture_output=True)
    assert r.returncode == 0, f'failed to delete resource: {r!r}'

@then(u'database "{db}" exists')
def step_impl(context, db):
    context.cleanup_databases.append(db)
    with context.db_cursor() as cur:
        for i in range(3):
            cur.execute(f"SHOW DATABASES LIKE '{db}'")
            r = cur.fetchone()
            if r is not None:
                assert r[0] == db, "database is not the same"
                break
            time.sleep(0.25)

@then(u'database "{db}" does not exist')
def step_impl(context, db):
    with context.db_cursor() as cur:
        for i in range(3):
            cur.execute(f"SHOW DATABASES LIKE '{db}'")
            r = cur.fetchone()
            if r is None:
                break
            time.sleep(0.25)
        assert r is None, "database exist"
