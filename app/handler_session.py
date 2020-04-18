import asyncio
from struct import *

from protomodels.packets_pb2 import PacketWrapper


class HandlerSession(asyncio.Protocol):
    def __init__(self, distributor):
        self.distributor = distributor
        self.transport = None
        self.is_new = False  # Is handler support new protocol with packet size

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data: bytes):
        try:
            magic, size = unpack(">BI", data[:5])
            if magic != 42:
                packet = PacketWrapper()
                packet.ParseFromString(data)
                print(packet)
                self.distributor.process_handler_message(packet.message, self)
                print("Packet successfully processed")
            else:
                print("Starting decoding new packet")
                self.is_new = True
                data = data[5:]
                while len(data) != 0:
                    packet = PacketWrapper()
                    print(''.join('{:02x}'.format(x) for x in data[:size]))
                    packet.ParseFromString(data[:size])
                    print("handle new pack {}".format(packet))
                    self.distributor.process_handler_message(packet.message, self)
                    if size < len(data):
                        print("decode more")
                        data = data[size:]
                        _, size = unpack(">BI", data[:5])
                        data = data[5:]
                    else:
                        break
        except Exception as e:
            print(e)

    def send(self, message):
        packet = PacketWrapper()
        packet.message.Pack(message)
        raw = packet.SerializeToString()
        if self.is_new:
            raw = pack(">I", len(raw)) + raw
        self.transport.write(raw)


async def create_handler_server(distributor, loop, host, port):
    return await loop.create_server(lambda: HandlerSession(distributor), host, port)
