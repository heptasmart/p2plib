import asyncio
import hashlib
from datetime import datetime

class NodeInfos:
    def __init__(self, ip, port, writer, reader):
        self.ip = ip
        self.port = port
        self.id =hashlib.sha224((ip + str(port)).encode('utf8')).hexdigest()
        self.writer = writer
        self.reader = reader
        self.lastHeartbeat = datetime.now()



class BaseNode:

    

    async def heartbeat_coro(self):

        while(True):
            for node_id in self.nodes:
                now = datetime.now()
                if now - nodes[node_id].lastHeartbeat > 10000:
                    print(node_id, " seems to be disconnected")
                nodes[node_id].send(Event("heartbeat", {"beat" : True}))
            
            await asyncio.sleep(5)

    async def heartbeat_receive(self, event):

        self.nodes[event.sender].lastHeartbeat = datetime.now()
        

    async def send(self, event, node_id):

        data = pickle.dumps(event)

        await self.nodes[node_id].writer.write(data)

        await self.nodes[node_id].writer.drain()


    async def receive_coro(self,reader, writer):
        while(True):
            data = await reader.read(1000)      
            try:
                event = pickle.loads(data)
            except EOFError:
                continue
            if event.name in self.event_handlers:

                addr = writer.get_extra_info('peername')
                node_id = hashlib.sha224(addr(0) + str(addr(1))).hexdigest()
                event.sender = self.nodes[node_ids]
                self.event_handlers[event.name](event)

            addr = writer.get_extra_info('peername')
            print("peername read")
            print(f"Received {event.name!r} from {addr!r}")

    def on(self, event, coro): 
        self.event_handlers[event] = coro

    def __init__(self):
        self.event_handlers = {}
        self.nodes = {}
        asyncio.create_task(self.heartbeat_coro())
        self.on("heartbeat", self.heartbeat_receive)
    
    

   