import time
import argparse
from ClientComponents.SinkClient import SinkClient
from ClientComponents.InternalController import InternalController
from interfaces.ttypes import ElementType, ElementState
from tensorflow.keras.preprocessing.image import ImageDataGenerator, DirectoryIterator
import numpy as np

IP_MASTER = "localhost"
MASTER_PORT = 10100
IMAGES_SOURCE = './images_source/'
BATCH_SIZE = 8
NO_IMAGES = 1000


class RemoteEdge:
    def __init__(self,  server_ip=IP_MASTER, port=MASTER_PORT):
        self.controller = InternalController(ElementType.CLIENT, server_ip=server_ip, port=port)
        self.controller.connect_to_configuration_server()
        self.controller.register_controller()
        self.remote_configurations = self.controller.get_servers_configuration().elements_configuration
        cloud_server = self.get_server_from_configuration(ElementType.CLOUD)
        self.sink_client = SinkClient(cloud_server.ip, cloud_server.port)
        self.sink_client.connect_to_sink_service()
        self.keras_model = self.controller.download_model()
        input_dimension = tuple(self.keras_model.layers[1].input_shape[1:3])
        self.test = self.controller.get_test()
        if self.test.is_test:
            self.batch_size = self.test.edge_batch_size
            self.no_images = self.test.number_of_images
        else:
            self.batch_size = BATCH_SIZE
            self.no_images = NO_IMAGES
        self.datagen = DataGenerator(IMAGES_SOURCE, ImageDataGenerator(), batch_size=self.batch_size,
                                     target_size=input_dimension, interpolation="nearest")

    def get_server_from_configuration(self, type: ElementType):
        for server_config in self.remote_configurations:
            if type == server_config.type:
                return server_config

    def run(self):
        images_read = 0
        while self.controller.update_state() == ElementState.RUNNING:
            data_batch, filenames = next(self.datagen)
            start = time.time()
            predicted = self.keras_model.predict(data_batch)
            end = time.time()
            self.sink_client.put_partial_result(filenames, predicted)
            self.controller.log_performance_message(self.batch_size, images_ids=filenames, elapsed_time=end-start)
            images_read += self.batch_size
            if images_read >= self.no_images:
                #something like test completed like ready state
                self.controller.set_state(ElementState.RESET)

        if self.controller.current_state == ElementState.RESET:
            self.controller.send_log("Disconnecting from all other server")
            self.sink_client.disconnect_from_sink_service()
            self.controller.send_log("Waiting a new model from master server")
            return 0

        if self.controller.current_state == ElementState.STOP:
            self.controller.send_log("Shutting down the mobile device")
            return 1


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
    result = 0
    while result == 0:
        client = RemoteEdge()
        result = client.run()
