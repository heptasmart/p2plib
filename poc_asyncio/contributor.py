from contributor_node import ContributorNode
import asyncio
from event import Event
try:
    import wmi
except ImportError:
    print("Need to be on windows to import this module")
import platform
import sys
import requests

class Contributor():

    async def job_proposal_handler(self, event):
        if self.working == True:
            nodeId = event.sender
            await self.node.send(Event("job_reponse", {'accepted': False}), nodeId)

        else:
            nodeId = event.sender
            await self.node.send(Event("job_reponse", {'accepted': True}), nodeId)
            getSystemInfo()
            self.node.send(
                Event("system_informatons", self.systemInfo), nodeId)

    async def start(self):

        requests.post("http://" + self.relay_address + ":8080")

    """Constructor for the contributor class"""

    def __init__(self, relay_address: str):
        self.node = ContributorNode()
        asyncio.create_task(self.node.start())
        self.working = False
        self.node.on('job_proposal', self.job_proposal_handler)
        self.systemInfo = {}
        self.relay_address = relay_address

    """getSystemInfo add cpu, ram and gpu specs to systemInfo"""

    def getSystemInfo(self):
        if platform.system() == "Windows":
            computer = wmi.WMI()
            computer_info = computer.Win32_ComputerSystem()[0]
            os_info = computer.Win32_OperatingSystem()[0]
            proc_info = computer.Win32_Processor()[0]
            gpu_info = computer.Win32_VideoController()[0]

            self.systemInfo['processor'] = platform.processor()
            self.systemInfo['ram'] = str(
            round(psutil.virtual_memory().total / (1024.0 ** 3)))+" GB"


if __name__ == "__main__":

    relay_host = "127.0.0.1"

    if len(sys.argv) > 1:
        relay_host = sys.argv[1]

    async def main():
        """
        """
        c = Contributor(relay_host)
        await c.start()

    asyncio.get_event_loop().create_task(main())
    asyncio.get_event_loop().run_forever()
