import json

from protomodels.packets_pb2 import Packet, Register, Result


class PacketDistributor:
    def __init__(self):
        self.handlers = {}
        self.sessions = {}

    def process_ws_packet(self, pack, sender):
        if sender.id not in self.sessions:
            self.sessions[sender.id] = sender

        pack = json.loads(pack)
        if pack['handler'] in self.handlers:
            packet = Packet()
            packet.user_id = sender.id
            packet.is_auth = True
            packet.data = json.dumps({'command': pack['command'], 'data': pack['data']})
            self.handlers[pack['handler']].send(packet)

    def process_handler_message(self, pack, sender):
        handlers = {Packet: self.process_handler_packet, Register: self.process_handler_register}
        for t in handlers.keys():
            if pack.Is(t.DESCRIPTOR):
                p = t()
                pack.Unpack(p)
                handlers[t](p, sender)

    def process_handler_packet(self, pack, sender):
        if pack.user_id in self.sessions:
            self.sessions[pack.user_id].send(json.dumps({'handler': sender.name, **json.loads(pack.data)}))

    def process_handler_register(self, pack, sender):
        self.handlers[pack.name] = sender
        sender.name = pack.name
        res = Result()
        res.status = Result.Status.SUCCESS
        sender.send(res)
