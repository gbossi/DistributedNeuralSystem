import threading
import time

from ClientComponents.InternalController import InternalController
from ServerComponents.SinkServer import SinkInterfaceService
from interfaces import SinkInterface
from interfaces.ttypes import ElementType, ElementState
from utils.thrift_servers import Server, ServerType

BATCH_DIM = 8
IP_SINK = "localhost"
SINK_PORT = 20200
IP_MASTER = "localhost"
MASTER_PORT = 10100


class CloudServer(threading.Thread):
    def __init__(self, sink: SinkInterfaceService):
        super(CloudServer, self).__init__()
        self.controller = InternalController(ElementType.CLOUD, server_ip=IP_MASTER, port=MASTER_PORT)
        self.controller.connect_to_configuration_server()
        self.cloud_model = self.controller.download_model()
        self.sink = sink
        self.controller.register_controller(server_ip=IP_SINK, server_port=SINK_PORT)


    def run(self):
        self.controller.set_state(ElementState.RUNNING)
        while self.controller.update_state() == ElementState.RUNNING:
            if self.sink.queue.qsize() >= BATCH_DIM:
                id_list, data_batch = self.sink.get_partial_result(BATCH_DIM)
                start = time.time()
                predicted = self.cloud_model.predict(data_batch)
                end = time.time()
                self.controller.send_log(str(end-start) + id_list)
            if self.sink.queue.qsize() == 0:
                time.sleep(3)
                print('Sleeping')

        if self.controller.current_state == ElementState.RESET:
            self.controller.send_log("Waiting a new model from master server")
            self.reconfigure()


    def reconfigure(self):
        self.cloud_model = self.controller.download_model()


if __name__ == '__main__':
    service = SinkInterfaceService()
    processor = SinkInterface.Processor(service)
    cloud_server = CloudServer(sink=service)
    cloud_server.start()
    print("Cloud Server Started")

    server = Server(ServerType.THREADED, processor, port=SINK_PORT)
    print("Sink Server Started")
    server.serve()
