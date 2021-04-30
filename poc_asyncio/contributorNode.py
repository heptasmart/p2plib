# Accept and maintain connections
# Advertise self to relays so new users can connect
import asyncio
import pickle
from event import Event
from basenode import BaseNode, NodeInfos


class ContributorNode(BaseNode):
    """
    This class adds some specific methods used by contributors. 
    It inherits the BaseNode class for receiving and sending messages, and maintaining connections.
    """

    def __init__(self,  relay_address, port=8888, interface="0.0.0.0"):
        """
        Constructor for the Contributor class.
        Calls super-constructor and sets port, interface, relay address and initializes user list.
        """
        super().__init__()
        self.port = port
        self.interface = interface
        self.relay_address = relay_address


    async def handle_connection(self, reader, writer):
        """
        Handler method for new connections.
        Adds the new node in the node dictionary and creates a task to handle messsages from the new node.
        """
        addr = writer.get_extra_info('peername')
        node = NodeInfos(addr[0], addr[1], writer, reader)
        self.nodes[node.id] = node
        print(node.ip, node.port, node.id)
        await asyncio.create_task(self.receive_coro(reader, writer))

    async def start(self):

        """
        Starts the contributor node with the connection handler method and network parameters.
        """
        server = await asyncio.start_server(
            self.handle_connection, self.interface, self.port)
        self.server = server
        
        relay_reader, relay_writer = await asyncio.open_connection(relay_address, 8889)
        relay = NodesInfos(relay_address, 8889, relay_writer, relay_reader)
        self.nodes[relay.id] = relay

        self.send(Event("contributor_available", {}), relay.id)

        async with server:
            await server.serve_forever()


if __name__ == "__main__":
    """
    If the class file is called as the main class,
    creates a contributor and starts on a default address.
    """

    async def main():
        c = ContributorNode("")
        await c.start()

    asyncio.run(main())
