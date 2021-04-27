# Asks relays for known servers and connect to them
import asyncio
from event import Event
from basenode import BaseNode, NodeInfos
import pickle

class User(BaseNode):

    def __init__(self, port=8888):
        super().__init__()
        self.port = port
        self.event_handlers = {}

    async def add_contributor(self, address):


        reader, writer = await asyncio.open_connection(
        address, self.port)

        node = NodeInfos(address, self.port, writer, reader)
        self.nodes[node.id] = node

        asyncio.create_task(self.receive_coro(reader, writer))
        #await asyncio.sleep(2)
        # event = Event("hello", {})
        # event2 = Event("bye", {})
        
        # await self.send(event, node.id)
        # await self.send(event2, node.id)
        """writer.write(pickle.dumps(event))
        await writer.drain()

        await asyncio.sleep(1)

        writer.write(pickle.dumps(event2))
        await writer.drain()
        writer.close()"""

    """async def receive_coro(self,reader, writer):
        while(True):
            data = await reader.read(10000)
            event = pickle.load(data)
            #message = data.decode()
            addr = writer.get_extra_info('peername')
            print(f"Received {event.name!r} from {addr!r}")"""

    def on(self, event, coro): 
        self.event_handlers[event] = coro

    async def start(self, server):
        await self.add_contributor(server)
        
        #reader, writer = await asyncio.open_connection(
        #relay_address, port)
        

if __name__ == "__main__":

    async def main():        
        u = User()
        await u.start("127.0.0.1")

    asyncio.run(main())