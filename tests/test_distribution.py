from packet_distributor import PacketDistributor
from protomodels.packets_pb2 import Register, Result, PacketWrapper, Packet
import json


def create_pack(pack, **kwargs):
    p = pack()
    [setattr(p, n, v) for n, v in kwargs.items()]
    return p


def pack_packet(packet):
    msg = PacketWrapper()
    msg.message.Pack(packet)
    pmsg = PacketWrapper()
    pmsg.ParseFromString(msg.SerializeToString())
    return msg


class TestSession:
    def __init__(self, id=1):
        self.messages = []
        self.id = id
        self.name = ''

    def send(self, msg):
        self.messages.append(msg)


def test_distribution():
    dist = PacketDistributor()
    handler_session = TestSession()
    dist.process_handler_message(pack_packet(create_pack(Register, name='test', only_auth=True)).message, handler_session)
    assert len(handler_session.messages) == 1
    assert handler_session.messages[0] == create_pack(Result, status=Result.Status.SUCCESS)
    assert handler_session.only_auth

    client_session = TestSession()
    dist.process_ws_connection(client_session)
    assert 1 in dist.sessions
    assert dist.sessions[1] == client_session
    assert handler_session.messages[1] == create_pack(Packet, is_auth=True, user_id=1, data='connected')
    dist.process_ws_packet(json.dumps({'handler': 'test', 'command': 'send_message', 'data': '123'}), client_session)
    assert handler_session.messages[2] == create_pack(Packet, is_auth=True, user_id=1, data=json.dumps({'command': 'send_message', 'data': '123'}))

    dist.process_handler_message(pack_packet(create_pack(Packet, user_id=1, data=json.dumps({'command': 'send_message', 'data':'123'}))).message,
                                 handler_session)
    assert len(client_session.messages) == 1
    assert client_session.messages[0] == json.dumps({'handler': 'test', 'command': 'send_message', 'data': '123'})

    client_session = TestSession(-1)
    dist.process_ws_connection(client_session)
    assert -1 in dist.sessions
    assert dist.sessions[-1] == client_session
    print(handler_session.messages)
    assert len(handler_session.messages) == 3

    dist.process_ws_packet(json.dumps({'handler': 'test', 'command': 'send_message', 'data': '123'}), client_session)
    assert len(handler_session.messages) == 3
