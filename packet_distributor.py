import json

from protomodels.packets_pb2 import Packet, Register, Result


class PacketDistributor:
    def __init__(self):
        self.handlers = {}
        self.sessions = {}

    @staticmethod
    def create_pack(sender, data):
        packet = Packet()
        packet.user_id = sender.id
        packet.is_auth = sender.id > 0
        packet.data = data
        return packet

    def process_ws_packet(self, pack, sender):
        pack = json.loads(pack)
        if pack['handler'] in self.handlers:
            self.handlers[pack['handler']]\
                .send(self.create_pack(sender, json.dumps({'command': pack['command'], 'data': pack['data']})))
        else:
            print("Unknown handler {}".format(pack['handler']))

    def process_ws_connection(self, sender):
        if sender.id == -1:
            sender.id = min(list(filter(lambda x: x < 0, self.sessions.keys())))-1
        self.sessions[sender.id] = sender
        pack = self.create_pack(sender, 'connected')
        [h.send(pack) for h in self.handlers.values()]

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
        print('Successfully registered {} handler'.format(pack.name))
