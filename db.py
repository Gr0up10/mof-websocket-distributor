import psycopg2
import os


class DB:
    def __init__(self, host, user, password, db):
        self.conn = None
        self.cur = None
        self.connect(host, user, password, db)

    def connect(self, host, user, password, db):
        self.conn = psycopg2.connect(dbname=db, user=user, password=password, host=host)
        self.cur = self.conn.cursor()

    def get_session_data(self, sessionid):
        self.cur.execute("SELECT session_data FROM django_session WHERE session_key=%s", (sessionid,))
        return self.cur.fetchone()[0]
