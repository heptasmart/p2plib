from contributorNode import ContributorNode
import asyncio
from event import Event
import wmi

class contributor():
    

    async def job_proposal_handler(self,event):
        if self.working==True:
            nodeId = event.sender
            await self.node.send(Event("job_reponse",{'accepted'=False}),nodeId)
            


        else:
            nodeId = event.sender
            await self.node.send(Event("job_reponse",{'accepted'=True}),nodeId)
            getSystemInfo()
            self.node.send(Event("system_informatons",self.systemInfo),nodeId)
    
    
    """Constructor for the contributor class"""
    
    def __init__(self,relay_address, port, interface):
            self.node=ContributorNode(relay_address,port,interface)
            asyncio.create_task(self.node.start()) 
            self.working=False
            self.node.on('job_proposal',self.job_proposal_handler)
            self.systemInfo={}
    
    
    """getSystemInfo add cpu, ram and gpu specs to systemInfo"""
    def getSystemInfo(self):
            computer = wmi.WMI()
            computer_info = computer.Win32_ComputerSystem()[0]
            os_info = computer.Win32_OperatingSystem()[0]
            proc_info = computer.Win32_Processor()[0]
            gpu_info = computer.Win32_VideoController()[0]

            self.systemInfo['processor']=platform.processor()
            self.systemInfo['ram']=str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"

       

