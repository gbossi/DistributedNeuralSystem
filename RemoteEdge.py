# Cloud Client
# Connect to Cloud server

# Send the prediction to the cloud
# Check the state

import time

from ClientComponents.SinkClient import SinkClient
from ClientComponents.InternalController import InternalController
from interfaces.ttypes import ElementType, ElementState
from tensorflow.keras.preprocessing.image import ImageDataGenerator, DirectoryIterator
import numpy as np

IP_MASTER = "localhost"
MASTER_PORT = 10100
IMAGES_SOURCE = './images_source/'
BATCH_SIZE = 8


class RemoteEdge:
    def __init__(self):
        self.controller = InternalController(ElementType.CLIENT, server_ip=IP_MASTER, port=MASTER_PORT)
        self.controller.connect_to_configuration_server()
        self.controller.register_controller()
        self.remote_configurations = self.controller.get_servers_configuration().elements_configuration
        cloud_server = self.get_server_from_configuration(ElementType.CLOUD)
        self.sink_client = SinkClient(cloud_server.ip, cloud_server.port)
        self.sink_client.connect_to_sink_service()
        self.keras_model = self.controller.download_model()
        # TODO log summary of the model maybe better in internal controller
        input_dimension = tuple(self.keras_model.layers[1].input_shape[1:3])
        self.datagen = DataGenerator(IMAGES_SOURCE, ImageDataGenerator(), batch_size=BATCH_SIZE,
                                     target_size=input_dimension, interpolation="nearest")

    def send_log(self, message):
        self.controller.send_log(message)

    def get_server_from_configuration(self, type: ElementType):
        for server_config in self.remote_configurations:
            if type == server_config.type:
                return server_config

    def run(self):
        # TODO following line to be removed
        i = 0
        while self.controller.update_state() == ElementState.RUNNING:
            data_batch, filenames = next(self.datagen)

            start = time.time()
            predicted = self.keras_model.predict(data_batch)
            end = time.time()
            self.sink_client.put_partial_result(filenames, predicted)
            self.controller.send_log(str(end-start) +"\n"+ str(filenames))
            # TODO following 3 lines to be removed
            i += 1
            if i == 10:
                exit()

        if self.controller.current_state == ElementState.RESET:
            self.controller.send_log("Disconnecting from all other server")
            self.sink_client.disconnect_from_sink_service()
            self.controller.send_log("Waiting a new model from master server")
            self.reconfigure()

        if self.controller.current_state == ElementState.STOP:
            self.controller.send_log("Shutting down the mobile device")
            self.controller.disconnect_to_configuration_server()

    def reconfigure(self):
        self.remote_configurations = self.controller.get_servers_configuration().elements_configuration
        cloud_server = self.get_server_from_configuration(ElementType.CLOUD)
        self.sink_client = SinkClient(cloud_server.ip, cloud_server.port)
        self.sink_client.connect_to_sink_service()
        self.keras_model = self.controller.download_model()
        # log summary of the model
        input_dimension = tuple(self.keras_model.layers[1].input_shape[1:3])
        self.datagen = DataGenerator(IMAGES_SOURCE, ImageDataGenerator(), batch_size=BATCH_SIZE,
                                     target_size=input_dimension, interpolation="nearest")
        self.run()


class DataGenerator(DirectoryIterator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filenames_np = np.array(self.filepaths)
        self.class_mode = None

    def _get_batches_of_transformed_samples(self, index_array):
        return (super()._get_batches_of_transformed_samples(index_array),
                self.filenames_np[index_array])


if __name__ == '__main__':
    client = RemoteEdge()
    client.run()
