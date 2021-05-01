from user_node import UserNode
import asyncio
from event import Event
import sys
import requests

class User():

    async def job_response_handler(self,event : Event):
        if event.data['accepted']==True:
            self.acceptedWorkers.append(event.sender)
        else:
            self.acceptedWorkers.remove(event.sender)

    async def send_proposal(self):
        
        for node_id in self.node.nodes.keys:
            await self.node.send(Event("job_proposal", {}), node_id)


    async def start(self):

        contributors = requests.get("http://" +self.relay_address + ":8080").json()
        for node_id in contributors:
            await self.node.add_contributor(contributors[node_id]["ip"])

    def __init__(self,relay_address : str):
        self.node = UserNode()
        self.relay_address = relay_address
        asyncio.create_task(self.node.start()) 
        self.acceptedWorkers=[]
        self.node.on('job_reponse',self.job_response_handler)
        #asyncio.create_task(self.sendProposal())

if __name__ == "__main__":

    relay_host = "127.0.0.1"

    if len(sys.argv) > 1:
        relay_host = sys.argv[1]

    async def main():
        """
        """
        u = User(relay_host)
        await u.start()

    asyncio.get_event_loop().create_task(main())
    asyncio.get_event_loop().run_forever()
