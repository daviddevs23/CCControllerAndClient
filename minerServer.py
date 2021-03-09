import websockets
import asyncio
import time
from botObject import Bot


async def open(websocket, path):
    
    bot = Bot(websocket)

    await bot.buildRoom(4,4,4)

    await bot.stop()


start_server = websockets.serve(open, "localhost", 8888)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
