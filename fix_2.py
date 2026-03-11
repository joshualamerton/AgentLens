# dashboard/server.py

import asyncio
import websockets
import json
from core.event_stream import EventStream

class DashboardServer:
    def __init__(self):
        self.event_stream = EventStream()
        self.clients = set()

    async def register(self, websocket):
        self.clients.add(websocket)
        try:
            await self.distribute_events(websocket)
        finally:
            await self.deregister(websocket)

    async def deregister(self, websocket):
        self.clients.remove(websocket)

    async def distribute_events(self, websocket):
        async for event in self.event_stream:
            await websocket.send(json.dumps(event))

    async def handle_client(self, websocket, path):
        await self.register(websocket)

    def start(self):
        start_server = websockets.serve(self.handle_client, "localhost", 8765)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    server = DashboardServer()
    server.start()