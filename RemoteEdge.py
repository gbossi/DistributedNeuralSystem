import time
import argparse
from ClientComponents.SinkClient import SinkClient
from ClientComponents.InternalController import InternalController
from interfaces.ttypes import ElementType, ElementState, Configuration
from tensorflow.keras.preprocessing.image import ImageDataGenerator, DirectoryIterator
import numpy as np

IP_MASTER = "localhost"
MASTER_PORT = 10100
IMAGES_SOURCE = './images_source/'
BATCH_SIZE = 8
NO_IMAGES = 1000


class RemoteEdge:
    def __init__(self, server_ip=IP_MASTER, port=MASTER_PORT):
        self.controller = InternalController(server_ip=server_ip, port=port)
        self.controller.register_element(ElementType.CLIENT)
        self.keras_model = self.controller.download_model()
        cloud_server = self.controller.get_element_type_from_configuration(self.controller.get_servers_configuration(),
                                                                           ElementType.CLOUD)[0]
        self.sink_client = SinkClient(cloud_server.ip, cloud_server.port)
        self.sink_client.connect_to_sink_service()

        self.test = self.controller.get_test()
        if self.test.is_test:
            self.batch_size = self.test.edge_batch_size
            self.no_images = self.test.number_of_images
        else:
            self.batch_size = BATCH_SIZE
            self.no_images = NO_IMAGES

    def run(self):
        input_dimension = tuple(self.keras_model.layers[1].input_shape[1:3])
        datagen = DataGenerator(IMAGES_SOURCE, ImageDataGenerator(), batch_size=self.batch_size,
                                target_size=input_dimension, interpolation="nearest")
        if self.test.is_test:
            self.run_test(datagen)
        else:
            self.run_edge(datagen)

        if self.controller.current_state == ElementState.READY:
            self.controller.wait_in_ready_state()

        if self.controller.current_state == ElementState.RUNNING:
            self.controller.send_log("Starting a new test with same configuration")

        if self.controller.current_state == ElementState.RESET:
            self.controller.send_log("Disconnecting from all other server")
            self.sink_client.disconnect_from_sink_service()
            self.controller.send_log("Waiting a new model from master server")

        if self.controller.current_state == ElementState.STOP:
            self.controller.send_log("Shutting down the mobile device")

        return self.controller.current_state

    def run_test(self, datagen):
        images_read = 0
        self.controller.send_log("Starting a new test")

        while self.controller.update_state() == ElementState.RUNNING:
            data_batch, filenames = next(datagen)
            start = time.time()
            predicted = self.keras_model.predict(data_batch)
            end = time.time()
            self.sink_client.put_partial_result(filenames, predicted)
            self.controller.log_performance_message_and_shape(self.batch_size, images_ids=filenames,
                                                              elapsed_time=end-start, shape=predicted.shape)
            images_read += self.batch_size
            if images_read >= self.no_images:
                self.controller.test_completed()
                self.controller.set_state(ElementState.READY)

    def run_edge(self, datagen):
        self.controller.send_log("Starting edge, running until status change")

        while self.controller.update_state() == ElementState.RUNNING:
            data_batch, filenames = next(datagen)
            start = time.time()
            predicted = self.keras_model.predict(data_batch)
            end = time.time()
            self.sink_client.put_partial_result(filenames, predicted)
            self.controller.log_performance_message_and_shape(self.batch_size, images_ids=filenames,
                                                              elapsed_time=end-start, shape=predicted.shape)


class DataGenerator(DirectoryIterator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filenames_np = np.array(self.filepaths)
        self.class_mode = None

    def _get_batches_of_transformed_samples(self, index_array):
        return (super()._get_batches_of_transformed_samples(index_array),
                self.filenames_np[index_array])


if __name__ == '__main__':
    '''
    parser = argparse.ArgumentParser(description=welcome)
    parser.add_argument('--master-ip', '-mip', required=True,
                        help='define the ip of the master server i.e. 192.168.1.125"')
    parser.add_argument('--master-port', '-mpo', required=True,
                        help='define the port of the master server i.e. 10100"', type=int)
    parser.add_argument('--images-source', '-is',
                        help='folder containing the input images"')
    parser.parse_args()

    args = parser.parse_args()

    master_ip = args.domain
    master_port = args.ofile
    images_source = args.lines

    client = RemoteEdge(server_ip=master_ip, port=master_port)
    '''
    result = ElementState.RUNNING
    client = RemoteEdge()
    while result != ElementState.STOP:
        result = client.run()
        if result == ElementState.RESET:
            client = RemoteEdge()
