import os

DB_NAME = os.getenv('DB_NAME', 'not found')
DB_HOST = os.getenv('DB_HOST', 'not found')
DB_USER = os.getenv('DB_USER', 'not found')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'not found')

DJANGO_SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'not found')

HANDLER_HOST = os.getenv('HANDLER_HOST', 'not found')
HANDLER_PORT = os.getenv('HANDLER_PORT', 'not found')

WS_HOST = os.getenv('WS_HOST', 'not found')
WS_PORT = os.getenv('WS_PORT', 'not found')
