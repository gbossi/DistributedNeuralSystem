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


class CloudThread(threading.Thread):
    def __init__(self, sink: SinkInterfaceService, sink_server: Server):
        super(CloudThread, self).__init__()
        self.server = sink_server
        self.sink = sink

    def run(self):
        result = 0
        while result == 0:
            cloud = CloudServer(sink=self.sink)
            result = cloud.run()
        self.server.stop()


class CloudServer():
    def __init__(self, sink: SinkInterfaceService):
        self.controller = InternalController(ElementType.CLOUD, server_ip=IP_MASTER, port=MASTER_PORT)
        self.controller.connect_to_configuration_server()
        self.cloud_model = self.controller.download_model()
        self.sink = sink
        self.controller.register_controller(server_ip=IP_SINK, server_port=SINK_PORT)
        self.test = self.controller.get_test()

    def run(self):
        self.controller.set_state(ElementState.RUNNING)

        while self.controller.update_state() == ElementState.RUNNING:
            if self.sink.queue.qsize() >= BATCH_DIM:
                id_list, data_batch = self.sink.get_partial_result(BATCH_DIM)
                start = time.time()
                predicted = self.cloud_model.predict(data_batch)
                end = time.time()
                self.controller.send_log(str(end-start) + "\n" + str(id_list))
            elif self.sink.queue.qsize() > 0:
                id_list, data_batch = self.sink.get_partial_result(self.sink.queue.qsize())
                start = time.time()
                predicted = self.cloud_model.predict(data_batch)
                end = time.time()
                self.controller.send_log(str(end-start) + "\n" + str(id_list))
            elif self.sink.queue.qsize() == 0:
                time.sleep(3)

        if self.controller.current_state == ElementState.RESET:
            self.controller.send_log("Waiting a new model from master server")
            return 0

        if self.controller.current_state == ElementState.STOP:
            self.controller.send_log("Waiting a new model from master server")
            return 1


if __name__ == '__main__':
    service = SinkInterfaceService()
    processor = SinkInterface.Processor(service)
    server = Server(ServerType.THREADED, processor, port=SINK_PORT)
    cloud_thread = CloudThread(sink=service, sink_server=server)
    cloud_thread.start()
    server.serve()



