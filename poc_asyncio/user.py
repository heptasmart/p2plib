from user_node import UserNode
import asyncio
from event import Event
import sys

class User():

    async def job_response_handler(self,event : Event):
        if event.data['accepted']==True:
            self.acceptedWorkers.append(event.sender)
        else:
            self.acceptedWorkers.remove(event.sender)

    async def sendProposal(self):
        
        for node_id in self.node.nodes.keys:
            await self.node.send(Event("job_proposal", {}), node_id)

    async def available_contributors_handler(self, event : Event):

        for node_id in event.data:
            await self.node.add_contributor(event.data[node_id]["ip"])
        print(event.data)
        print(self.node.nodes)

    async def start(self):

        self.node.on("available_contributors", self.available_contributors_handler)

        await self.node.connect_relay(self.node.relay_address)
        await self.node.send(Event("user_connected", {}), self.node.relay_id)

    def __init__(self,relay_address : str):
        self.node = UserNode(relay_address)
        
        asyncio.create_task(self.node.start()) 
        self.acceptedWorkers=[]
        self.node.on('job_reponse',self.job_response_handler)
        #asyncio.create_task(self.sendProposal())

if __name__ == "__main__":

    relay_host = "127.0.0.1"

    if len(sys.argv) > 0:
        relay_host = sys.argv[1]

    async def main():
        """
        """
        u = User(relay_host)
        await u.start()

    asyncio.get_event_loop().create_task(main())
    asyncio.get_event_loop().run_forever()
