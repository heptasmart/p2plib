import asyncio
from event import Event
from basenode import BaseNode, NodeInfos
import pickle


class User(BaseNode):
    """
    This class adds some specific methods used by users. 
    It inherits the BaseNode class for receiving and sending messages, and maintaining connections.
    """

    def __init__(self, relay_address, port=8888):

        """
        Constructor for the User class.
        Calls super-constructor and sets port.
        """
        super().__init__()
        self.port = port
        self.on("available_contributors", self.available_contributors_coro)
        self.relay_address = relay_address

    def available_contributors_coro(self, event):

        for node_id in event.data.keys:
            await self.add_contributor(event.data[node_id].ip)

    async def add_contributor(self, address):

        """
        Connects to a known contributor.
        BaseNode methods will be used to maintain all connections.
        Relay nodes give information on known nodes, but User nodes have to manage down contributors.
        """

        reader, writer = await asyncio.open_connection(
            address, self.port)

        node = NodeInfos(address, self.port, writer, reader)
        self.nodes[node.id] = node
        print(node.ip, node.port, node.id)
        asyncio.get_event_loop().create_task(self.receive_coro(reader, writer))


    async def start(self, server):
        """Starts the User node."""
        #await self.add_contributor(server)
        relay_reader, relay_writer = await asyncio.open_connection(self.relay_address, 8889)
        relay = NodeInfos(relay_address, 8889, relay_writer, relay_reader)
        self.nodes[relay.id] = relay

        self.send(Event("user_connected", {}), relay.id)



if __name__ == "__main__":
    """
    If the class file is called as the main class,
    creates a user and starts on a default address.
    """

    async def main():
        """
        """
        u = User()
        await u.start("127.0.0.1")

    asyncio.get_event_loop().create_task(main())
    asyncio.get_event_loop().run_forever()
