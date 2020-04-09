from db import DB
import datetime
import constants


def test_db():
    db = DB()
    db.connect(constants.DB_HOST, constants.DB_USER, constants.DB_PASSWORD, constants.DB_NAME)
    db.cur.execute("INSERT INTO django_session (session_key, session_data, expire_date) VALUES (%s, %s, %s)", ('123', "321", datetime.datetime.now()))
    assert db.get_session_data('123') == '321'
