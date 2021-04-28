import asyncio
import hashlib
import pickle
from datetime import datetime

from event import Event

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
                
                if (now - self.nodes[node_id].lastHeartbeat).total_seconds() > 10:
                    print(node_id, "seems to be disconnected")
                
                await self.send(Event("heartbeat", {"beat" : True}), node_id)
            
            await asyncio.sleep(5)

    async def heartbeat_receive(self, event):

        self.nodes[event.sender].lastHeartbeat = datetime.now()
        

    async def send(self, event, node_id):

        print("Send", event.name, "to", self.nodes[node_id].ip, ':', self.nodes[node_id].port)

        data = pickle.dumps(event)

        self.nodes[node_id].writer.write(data)

        await self.nodes[node_id].writer.drain()


    async def receive_coro(self,reader, writer):
        while(True):
            data = await reader.read(1000)      
            try:
                event = pickle.loads(data)
            except EOFError as e:
                print(e)
                continue
            if event.name in self.event_handlers:

                addr = writer.get_extra_info('peername')
                node_id = hashlib.sha224((addr[0] + str(addr[1])).encode()).hexdigest()
                event.sender = node_id
                await self.event_handlers[event.name](event)

            addr = writer.get_extra_info('peername')
            print(f"Received {event.name!r} from {addr!r}")

    def on(self, event, coro): 
        self.event_handlers[event] = coro

    def __init__(self):
        self.event_handlers = {}
        self.nodes = {}
        asyncio.get_event_loop().create_task(self.heartbeat_coro())  
        self.on("heartbeat", self.heartbeat_receive)
    
    

   