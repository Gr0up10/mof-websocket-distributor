import json

from protomodels.packets_pb2 import Packet


class PacketDistributor:
    def __init__(self):
        self.handlers = {}
        self.sessions = {}

    def process_ws_packet(self, pack, sender):
        pack = json.loads(pack)
        if pack.handler in self.handlers:
            packet = Packet()
            packet.user_id = 0
            packet.is_auth = True
            packet.data = json.dumps({'command': pack['command'], 'data': pack['data']})
            self.handlers[pack.handler].send(packet)
