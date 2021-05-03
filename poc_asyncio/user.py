from user_node import UserNode
import asyncio
from event import Event
import sys
import requests
import docker


class User():

    async def job_response_handler(self, event: Event):
        if event.data['accepted'] == True:
            self.accepted_workers[event.sender] = {
                "accepted": True, "ready": False}
            await self.send_parameters()
        else:
            self.accepted_workers.pop(event.sender, None)

    async def send_proposal(self):

        for node_id in self.node.nodes:
            await self.node.send(Event("job_proposal", {}), node_id)

    async def send_parameters(self):

        for node_id in self.accepted_workers:
            await self.node.send(Event("job_parameters", {"advertise_ip" : self.node.nodes[node_id].ip, "swarm_token": self.client.swarm.attrs['JoinTokens']['Worker'], "network_name": "spark-net", "docker_name": node_id}), node_id)

    async def worker_ready_handler(self, event: Event):

        if event.sender in self.accepted_workers:
            self.accepted_workers[event.sender]["ready"] = True

        everyone_is_ready = True

        for node_id in self.accepted_workers:
            if self.accepted_workers[node_id] == False:
                everyone_is_ready = False
                break

        if everyone_is_ready:
            print("Every worker is ready. Spark master instance is accesible at :")

    async def handle_deconnection(self, node_id):
        print("Disconneted from", node_id, ".Attempting to reconnected")

    async def start(self):

        contributors = requests.get(
            "http://" + self.relay_address + ":8888").json()
        for node_id in contributors:
            await self.node.add_contributor(contributors[node_id]["ip"])

        await self.send_proposal()
        # TODO
        # Start up the docker image, create swarm, create network
        self.client.swarm.leave(force=True)
        try:
            self.client.containers.list(filters ={ "name": "spark-master"})[0].remove(force=True)
        except :
            print('got no image to kill')
        self.client.swarm.init(advertise_addr=self.ADVERTISE_IP, listen_addr=self.LISTEN_IP)
        self.client.networks.create(name="spark-net", driver="overlay", attachable=True)
        self.client.containers.run(image='bde2020/spark-master:3.1.1-hadoop3.2',
                      detach=True,
                      name="spark-master",
                      environment=["SPARK_PUBLIC_DNS=" + self.ADVERTISE_IP, 
                                   "SPARK_MASTER_HOST=spark-master"],
                      ports={
                          		8080:8080,
                          		4040:4040
                            },
                      hostname="spark-master",
                      network="spark-net",
                      auto_remove=True)

    def __init__(self, relay_address: str, advertise_ip:str, listen_ip:str):
        self.node = UserNode()
        self.relay_address = relay_address
        asyncio.create_task(self.node.start())
        self.accepted_workers = {}
        self.node.on('job_reponse', self.job_response_handler)
        self.node.on("worker_ready", self.worker_ready_handler)
        self.swarm_token = ""
        self.network_name = ""
        self.ADVERTISE_IP = advertise_ip
        self.LISTEN_IP = listen_ip
        self.node.handle_deconnection = self.handle_deconnection
        self.client=docker.from_env()
        



if __name__ == "__main__":

    relay_host = "127.0.0.1"
    advertise_ip = ""
    listen_ip = ""
    if len(sys.argv) > 1:
        relay_host = sys.argv[1] 
        advertise_ip = sys.argv[2]
        listen_ip = sys.argv[3]

    async def main():
        """
        """
        u = User(relay_host, advertise_ip, listen_ip)
        await u.start()

    asyncio.get_event_loop().create_task(main())
    asyncio.get_event_loop().run_forever()
