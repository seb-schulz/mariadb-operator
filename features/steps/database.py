from behave import *
import subprocess
import time


@then(u'database "{db}" exists')
def step_impl(context, db):
    context.cleanup_databases.append(db)
    with context.db_cursor() as cur:
        for i in range(3):
            cur.execute("SHOW DATABASES LIKE %s", [db])
            r = cur.fetchone()
            if r is not None:
                assert r[0] == db, "database is not the same"
                break
            time.sleep(0.25)

@then(u'database "{db}" does not exist')
def step_impl(context, db):
    with context.db_cursor() as cur:
        for i in range(3):
            cur.execute("SHOW DATABASES LIKE %s", [db])
            r = cur.fetchone()
            if r is None:
                break
            time.sleep(0.25)
        assert r is None, "database exist"
