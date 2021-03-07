import websockets
import asyncio
import time

async def open(websocket, path):

    await websocket.send("fuelLevel")
    print(await websocket.recv())

    await websocket.send("refuel")
    print(await websocket.recv())

    await websocket.send("fuelLevel")
    print(await websocket.recv())

    await websocket.send("stop")

start_server = websockets.serve(open, "localhost", 8888)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
