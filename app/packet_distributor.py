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
            handler = self.handlers[pack['handler']]
            if not handler.only_auth or sender.id >= 0:
                handler.send(self.create_pack(sender, json.dumps({'command': pack['command'], 'data': pack['data']})))
        else:
            print("Unknown handler {}".format(pack['handler']))

    def process_ws_connection(self, sender):
        if sender.id == -1:
            sender.id = (min(list(filter(lambda x: x < 0, self.sessions.keys()))+[0]))-1
            print("Set id ", sender.id)
        self.sessions[sender.id] = sender
        print(self.sessions)
        pack = self.create_pack(sender, 'connected')
        [h.send(pack) for h in self.handlers.values() if not h.only_auth or sender.id >= 0]

    def process_ws_disconnection(self, sender):
        pack = self.create_pack(sender, 'disconnected')
        [h.send(pack) for h in self.handlers.values() if not h.only_auth or sender.id >= 0]
        del self.sessions[sender.id]

    def process_handler_message(self, pack, sender):
        handlers = {Packet: self.process_handler_packet, Register: self.process_handler_register}
        for t in handlers.keys():
            if pack.Is(t.DESCRIPTOR):
                print("find handler for packet", t)
                p = t()
                pack.Unpack(p)
                handlers[t](p, sender)
                return
        print("Cannot parse packet {}".format(pack))

    def process_handler_packet(self, pack, sender):
        print("Start processing packet")
        print(pack.user_id)
        user_id = pack.user_id
        #user_id = (user_id >> 1) ^ (-(user_id & 1))
        self.sessions[user_id].id = user_id
        print("Packet user id {} saved user id {}".format(user_id, self.sessions[user_id].id))
        if user_id in self.sessions:
            self.sessions[user_id].send(json.dumps({'handler': sender.name, **json.loads(pack.data)}))
        else:
            print("User id {} not found, sent from {} <{}>".format(user_id, sender.name, pack))

    def process_handler_register(self, pack, sender):
        self.handlers[pack.name] = sender
        sender.name = pack.name
        sender.only_auth = pack.only_auth
        res = Result()
        res.status = Result.Status.SUCCESS
        sender.send(res)
        print('Successfully registered {} handler'.format(pack.name))
