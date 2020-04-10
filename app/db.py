import psycopg2


class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DB(metaclass=MetaSingleton):
    def __init__(self):
        self.conn = None
        self.cur = None

    def connect(self, host, user, password, db):
        self.conn = psycopg2.connect(dbname=db, user=user, password=password, host=host)
        self.cur = self.conn.cursor()

    def get_session_data(self, sessionid):
        self.cur.execute("SELECT session_data FROM django_session WHERE session_key=%s", (sessionid,))
        return self.cur.fetchone()[0]
