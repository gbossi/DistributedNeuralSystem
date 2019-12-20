import threading
import time
import tensorflow as tf

from src.utils.thrift_servers import Server, ServerType
from tensorflow.keras.applications.imagenet_utils import decode_predictions
from src.components.client_components.internal_controller import InternalController
from src.components.server_components.sink_server import SinkInterfaceService

from interfaces import SinkInterface
from interfaces.ttypes import ElementType, ElementState

BATCH_SIZE = 8
NO_IMAGES = 1000
SINK_PORT = 20200


class CloudThread(threading.Thread):
    def __init__(self, master_ip, master_port, sink: SinkInterfaceService, sink_server: Server):
        super(CloudThread, self).__init__()
        self.master_ip = master_ip
        self.master_port = master_port
        self.server = sink_server
        self.sink = sink

    def run(self):
        result = ElementState.RUNNING
        cloud = CloudServer(self.master_ip, self.master_port, self.sink, self.server)
        while result != ElementState.STOP:
            result = cloud.run()
            if result == ElementState.RESET:
                cloud.reset_values()
        self.server.stop()


class CloudServer:
    def __init__(self, master_ip, master_port, sink: SinkInterfaceService, server):
        self.controller = InternalController(server_ip=master_ip, port=master_port)
        self.controller.register_element(ElementType.CLOUD, server_ip=server.ip, server_port=server.port)
        model_filename = self.controller.download_model()
        self.cloud_model = tf.keras.models.load_model(model_filename)
        self.sink = sink

        self.test = self.controller.get_test()
        if self.test.is_test:
            self.batch_size = self.test.edge_batch_size
            self.no_images = self.test.number_of_images
        else:
            self.batch_size = BATCH_SIZE
            self.no_images = NO_IMAGES

    def run(self):

        if self.test.is_test:
            self.run_test()
        else:
            self.run_cloud()

        if self.controller.current_state == ElementState.READY:
            self.controller.wait_in_ready_state()

        if self.controller.current_state == ElementState.RUNNING:
            self.controller.send_log("Starting a new test with same configuration")

        if self.controller.current_state == ElementState.RESET:
            self.controller.send_log("Waiting a new model from master server")

        if self.controller.current_state == ElementState.STOP:
            self.controller.send_log("Server stopped working")

        return self.controller.current_state

    def run_test(self):
        self.controller.send_log("Start processing images in queue")
        remaining_batch = self.batch_size
        test_started = False
        while self.controller.update_state() == ElementState.RUNNING:
            if self.sink.queue.qsize() >= remaining_batch:
                id_list, data_batch = self.sink.get_partial_result(self.batch_size)
                start = time.time()
                predicted = self.cloud_model.predict(data_batch)
                end = time.time()
                self.controller.log_performance_message(self.batch_size, images_ids=id_list, elapsed_time=end-start)
                remaining_batch = self.batch_size
                test_started = True
            else:
                time.sleep(3)
                current_size = self.sink.queue.qsize()
                remaining_batch = current_size if current_size > 0 else self.batch_size
                if self.sink.queue.empty() and test_started:
                    self.controller.test_completed()
                    self.controller.set_state(ElementState.READY)

    def run_cloud(self):
        self.controller.send_log("Start processing images in queue until stop status")
        remaining_batch = self.batch_size

        while self.controller.update_state() == ElementState.RUNNING:
            if self.sink.queue.qsize() >= remaining_batch:
                id_list, data_batch = self.sink.get_partial_result(self.batch_size)
                start = time.time()
                predicted = self.cloud_model.predict(data_batch)
                end = time.time()
                self.controller.log_performance_message(self.batch_size, images_ids=id_list, elapsed_time=end-start)
                remaining_batch = self.batch_size
            else:
                time.sleep(3)
                current_size = self.sink.queue.qsize()
                remaining_batch = current_size if current_size > 0 else self.batch_size

    def decode_prediction_batch(self, predicted):
        decoded = []
        for i in range(len(predicted)):
            decoded = decoded+[decode_predictions(predicted[i])]
        return decoded

    def reset_values(self):
        self.controller.set_state(ElementState.WAITING)
        model_filename = self.controller.download_model()
        self.cloud_model = tf.keras.models.load_model(model_filename)
        self.sink.reset_sink()
        self.test = self.controller.get_test()
        if self.test.is_test:
            self.batch_size = self.test.edge_batch_size
            self.no_images = self.test.number_of_images
        else:
            self.batch_size = BATCH_SIZE
            self.no_images = NO_IMAGES


def cloud_server_main(master_ip, master_port, sink_port=SINK_PORT):
    service = SinkInterfaceService()
    processor = SinkInterface.Processor(service)
    server = Server(ServerType.THREADED, processor, port=sink_port)
    cloud_thread = CloudThread(master_ip=master_ip, master_port=master_port, sink=service, sink_server=server)
    cloud_thread.start()
    server.serve()


if __name__ == '__main__':
    cloud_server_main('localhost', 10100, SINK_PORT)
