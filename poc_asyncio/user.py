from userNode import UserNode
import asyncio
from event import Event
class user():
    
    async def job_response_handler(self,event):
        if event.data['accepted']==True:
            self.acceptedWorkers.append(event.sender)
        else:
            self.acceptedWorkers.remove(event.sender)

    async def sendProposal(self):
        
        for node_id in self.node.nodes.keys:
            await self.node.send(Event("job_proposal", {}), node_id)

    def __init__(self,relay_address, port, interface):
            self.node=UserNode(relay_address,port,interface)
            asyncio.create_task(self.node.start()) 
            self.acceptedWorkers=[]
            self.on('job_reponse',self.job_reponse_handler)
            asyncio.create_task(self.sendProposal())

    