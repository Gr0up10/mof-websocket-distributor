from struct import pack

from app.handler_session import HandlerSession
from protomodels.packets_pb2 import PacketWrapper, Packet


class Sink:
    def __init__(self):
        self.messages = []

    def process_handler_message(self, pack, sender):
        self.messages.append(pack)


def test_serialization():
    sink = Sink()
    handler = HandlerSession(sink)

    message = Packet()
    packet = PacketWrapper()
    packet.message.Pack(message)
    raw = packet.SerializeToString()
    raw = pack(">BI", 42, len(raw)) + raw
    message = Packet(user_id=-2)
    packet = PacketWrapper()
    packet.message.Pack(message)
    raw2 = packet.SerializeToString()
    raw += pack(">BI", 42, len(raw2)) + raw2
    handler.data_received(raw)
    assert sink.messages[0].Is(Packet.DESCRIPTOR)
    p = Packet()
    sink.messages[0].Unpack(p)
    assert p.user_id == 0
    assert p.data == ''

    assert sink.messages[1].Is(Packet.DESCRIPTOR)
    p = Packet()
    sink.messages[1].Unpack(p)
    assert p.user_id == -2
    assert p.data == ''
