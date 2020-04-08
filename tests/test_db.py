from db import DB
import datetime


def test_db():
    db = DB('localhost', 'username', 'password', 'database')
    db.cur.execute("INSERT INTO django_session (session_key, session_data, expire_date) VALUES (%s, %s, %s)", ('123', "321", datetime.datetime.now()))
    assert db.get_session_data('123') == '321'