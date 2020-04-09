import asyncio

from protomodels.packets_pb2 import PacketWrapper


class HandlerSession(asyncio.Protocol):
    def __init__(self, distributor):
        self.distributor = distributor
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data: bytes):
        print(data)
        #data = data.decode('ascii')
        pack = PacketWrapper()
        pack.ParseFromString(data)
        self.distributor.process_handler_message(pack.message, self)

    def send(self, packet):
        pack = PacketWrapper()
        pack.message.Pack(packet)
        self.transport.write(pack.SerializeToString())


async def create_handler_server(distributor, loop, host, port):
    return await loop.create_server(lambda: HandlerSession(distributor), host, port)
