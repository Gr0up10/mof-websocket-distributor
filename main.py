import asyncio

import constants
from db import DB
from handler_session import create_handler_server
from ws_session import WSSession
from packet_distributor import PacketDistributor


async def main():
    DB().connect(constants.DB_HOST, constants.DB_USER, constants.DB_PASSWORD, constants.DB_NAME)

    loop = asyncio.get_event_loop()
    dist = PacketDistributor()
    serve = await WSSession(dist).create_server(constants.WS_HOST, constants.WS_PORT)
    ws_server = await serve
    handler_server = await create_handler_server(dist, loop, constants.HANDLER_HOST, constants.HANDLER_PORT)

    async with ws_server.server, handler_server:
        await asyncio.gather(
            ws_server.server.serve_forever(), handler_server.serve_forever())


if __name__ == "__main__":
    asyncio.run(main())
