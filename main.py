import asyncio
import websockets


async def ws_handler(websocket, path):
    print({c.split('=')[0]: c.split('=')[1] for c in websocket.request_headers['cookie'].split('; ')}['sessionid'])
    name = await websocket.recv()
    print(f"< {name}")

    greeting = f"Hello {name}!"

    await websocket.send(greeting)
    print(f"> {greeting}")


def main():
    start_server = websockets.serve(ws_handler, "localhost", 8765)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()