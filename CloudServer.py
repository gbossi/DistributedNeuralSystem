from ClientComponents.ControllerClient import ControllerClient
from ServerComponents.SinkServer import SinkInterfaceService
from interfaces.ttypes import ElementType, ElementState
from interfaces import SinkInterface
import threading, time
from utils.thrift_servers import Server, ServerType

BATCH_DIM = 8


class CloudServer(threading.Thread):
    def __init__(self, sink: SinkInterfaceService):
        super(CloudServer, self).__init__()
        self.controller = ControllerClient(ElementType.CLOUD, server_ip='localhost', port='10100')
        self.controller.connect_to_configuration_server()
        self.controller.register_controller("localhost", server_port=20200)
        self.cloud_model = self.controller.download_model()
        self.cloud_model.summary()
        self.sink = sink

    def run(self):
        self.controller.set_state(ElementState.RUNNING)
        print('running')
        while self.controller.get_state() == ElementState.RUNNING:
            if self.sink.queue.qsize() >= BATCH_DIM:
                id_list, data_batch = self.sink.get_partial_result(BATCH_DIM)
                start = time.time()
                predicted = self.cloud_model.predict(data_batch)
                end = time.time()
                self.controller.send_log(str(end-start))
                print(predicted)
            if self.sink.queue.qsize() == 0:
                time.sleep(3)
                print('sleeping')


if __name__ == '__main__':
    service = SinkInterfaceService()
    processor = SinkInterface.Processor(service)
    cloud_server = CloudServer(sink=service)
    cloud_server.start()
    print("Cloud Server Started")

    server = Server(ServerType.THREADED, processor, port=20200)
    print("Sink Server Started")
    server.serve()
