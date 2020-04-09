import psycopg2
import testing.postgresql


from db import DB
import datetime
import constants


def test_db():
    db = DB()
    with testing.postgresql.Postgresql() as postgresql:
        db.conn = psycopg2.connect(**postgresql.dsn())
        db.cur = db.conn.cursor()
        db.cur.execute("CREATE TABLE django_session (session_key varchar(255),session_data varchar(255),expire_date varchar(255))")
        db.cur.execute("INSERT INTO django_session (session_key, session_data, expire_date) VALUES (%s, %s, %s)", ('123', "321", datetime.datetime.now()))
        assert db.get_session_data('123') == '321'
