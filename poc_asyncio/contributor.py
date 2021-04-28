# Accept and maintain connections 
# Advertise self to relays so new users can connect T LA ?
import asyncio
import pickle
from event import Event
from basenode import BaseNode, NodeInfos
class Contributor(BaseNode): 
    def __init__(self,  relay_address, port=8888, interface="0.0.0.0"):
        super().__init__()
        self.port = port
        self.interface = interface
        self.relay_address = relay_address
        self.users = []
        

    async def handle_connection(self,reader, writer):
        addr = writer.get_extra_info('peername')
        node = NodeInfos(addr[0], addr[1], writer, reader)
        self.nodes[node.id] = node
        await asyncio.create_task(self.receive_coro(reader, writer))

    async def start(self):
        server = await asyncio.start_server(
        self.handle_connection, self.interface, self.port)
        self.server = server
        async with server:
            await server.serve_forever()

    

if __name__ == "__main__":

    def hello(event):
        print("world")
    def bye(event):
        print("bye bye", event.name)

    async def main():        
        c = Contributor("")
        c.on("hello", hello)
        c.on("bye", bye)
        await c.start()

    asyncio.run(main())
    