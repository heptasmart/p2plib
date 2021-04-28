# Store known contributors and give a list on user request
import asyncio
class Relay:

    def __init__(self,  relay_address, port=8888, interface="0.0.0.0"):
        self.port = port
        self.interface = interface
        self.relay_address = relay_address

    

    def start(self):
            self.server = await asyncio.start_server(
            handle_connection, self.interface, self.port)