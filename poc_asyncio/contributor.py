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
import docker

class Contributor():

    async def job_proposal_handler(self, event: Event):
        if self.working == True:
            nodeId = event.sender
            await self.node.send(Event("job_reponse", {'accepted': False}), nodeId)

        else:
            nodeId = event.sender
            await self.node.send(Event("job_reponse", {'accepted': True}), nodeId)
            # getSystemInfo()
            await self.node.send(
                Event("system_informatons", self.systemInfo), nodeId)
            self.current_master = nodeId

    async def job_parameters_handler(self, event: Event):

        if event.sender == self.current_master:
            self.swarm_token = event.data["swarm_token"]
            self.network_name = event.data["network_name"]
            self.docker_name = event.data["docker_name"]
            advertise_ip = event.data["advertise_ip"]
            # TODO
            # set-up docker and launch spark-woker
            self.client.swarm.join(remote_addrs=[self.node.nodes[event.sender].ip], join_token=swarm_token, advertise_addr=advertise_ip, listen_addr=self.LISTEN_IP)
            self.client.containers.run(image='bde2020/spark-worker:3.1.1-hadoop3.2',
                      detach=True,
                      name="spark-worker",
                      environment=["SPARK_PUBLIC_DNS=" + self.node.nodes[event.sender].ip],
                      ports={
                          		8081:8081
                            },
                      hostname=self.docker_name,
                      network="spark-net")
            await self.send_worker_ready()

    async def send_worker_ready(self):

        await self.node.send(Event("worker_ready", {}), self.current_master)

    async def start(self):

        requests.post("http://" + self.relay_address + ":8888")

    async def handle_deconnection(self, node_id):
        print("Disconnedted from master, available again")
        self.working = False

    """Constructor for the contributor class"""

    def __init__(self, relay_address: str, listen_ip:str)
        self.node = ContributorNode()
        asyncio.create_task(self.node.start())
        self.working = False
        self.node.on('job_proposal', self.job_proposal_handler)
        self.node.on("job_parameters", self.job_parameters_handler)
        self.systemInfo = {}
        self.relay_address = relay_address
        self.current_master = ""
        self.swarm_token = ""
        self.network_name = "spark-net"
        self.docker_name = ""
        self.node.handle_deconnection = self.handle_deconnection
        self.client=docker.from_env()
        self.LISTEN_IP=listen_ip

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
    listen_ip = ""
    if len(sys.argv) > 1:
        relay_host = sys.argv[1]
        listen_ip = sys.argv[2]

    async def main():
        """
        """
        c = Contributor(relay_host)
        await c.start()

    asyncio.get_event_loop().create_task(main())
    asyncio.get_event_loop().run_forever()
