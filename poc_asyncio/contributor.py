from contributorNode import ContributorNode
import asyncio
from event import Event
class contributor():
    
    async def job_proposal_handler(self,event):
        if self.working==True:
            nodeId = event.sender
            await self.node.send(Event("job_reponse",{'accepted'=False}),nodeId)

        else:
            nodeId = event.sender
            await self.node.send(Event("job_reponse",{'accepted'=True}),nodeId)

    def __init__(self,relay_address, port, interface):
            self.node=ContributorNode(relay_address,port,interface)
            asyncio.create_task(self.node.start()) 
            self.working=False
            self.node.on('job_proposal',self.job_proposal_handler)
