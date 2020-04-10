import asyncio
import websockets

from app import constants
from app.db import DB
from app import session_decoder


def parse_cookie(cookie):
    return {c.split('=')[0]: c.split('=')[1] for c in cookie.split('; ')}


class WSSession:
    def __init__(self, distributor):
        self.id = -1
        self.distributor = distributor
        self.socket = None

    async def ws_handler(self, websocket, path):
        self.socket = websocket
        try:
            session = parse_cookie(websocket.request_headers['cookie'])['sessionid']
            self.id = int(session_decoder.decode(DB().get_session_data(session), constants.DJANGO_SECRET_KEY)['_auth_user_id'])
        except Exception as e:
            print('auth failed {}'.format(e))

        if self.id != -1:
            print('Successfully authorized {}'.format(self.id))

        self.distributor.process_ws_connection(self)

        while True:
            pack = await websocket.recv()
            print('WS {} received {}'.format(self.id, pack))
            self.distributor.process_ws_packet(pack, self)

    def send(self, pack):
        print('send'+pack)
        asyncio.run_coroutine_threadsafe(self.socket.send(pack), asyncio.get_event_loop())

    async def create_server(self, host, port):
        start_server = websockets.serve(self.ws_handler, host, port)
        return start_server
