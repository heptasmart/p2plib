# Store known contributors and give a list on user request
import asyncio
from basenode import BaseNode
from event import Event
class Relay(BaseNode):


    async def contributor_available_coro(self, event):

        self.contributors[event.sender] = self.nodes[event.sender]
        print("Added contributor", event.sender)


    async def user_connected_coro(self, event):
        
        available = Event("available_contributors", self.contributors)
        await self.send(event.sender, available)
        print("Sent contributors to", event.sender)


    def __init__(self,  relay_address, port=8888, interface="0.0.0.0"):
        super().__init__()
        self.port = port
        self.interface = interface
        self.relay_address = relay_address
        self.contributors = {}
        self.on("contributor_available", contributor_available)
        self.on("user_connected", user_connected_coro)

    

    async def start(self):

        """
        Starts the contributor node with the connection handler method and network parameters.
        """
        server = await asyncio.start_server(
            self.handle_connection, self.interface, self.port)
        self.server = server
        async with server:
            await server.serve_forever()