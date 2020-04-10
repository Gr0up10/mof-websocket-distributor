import os

DB_NAME = os.getenv('DB_NAME', 'database')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'username')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')

DJANGO_SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'ecw==078()bm0#u^f6))--6jz3nk27rwy04wb6=2f_3rqrsvq*')

HANDLER_HOST = os.getenv('HANDLER_HOST', 'localhost')
HANDLER_PORT = os.getenv('HANDLER_PORT', '58008')

WS_HOST = os.getenv('WS_HOST', 'localhost')
WS_PORT = os.getenv('WS_PORT', '4321')
