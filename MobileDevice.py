# Cloud Client
# Connect to Cloud server

# Send the prediction to the cloud
# Check the state

import time

from ClientComponents.ControllerClient import ControllerClient
from interfaces.ttypes import ElementType, ElementState
from tensorflow.keras.preprocessing.image import ImageDataGenerator, DirectoryIterator
import numpy as np


class MobileDevice:
    def __init__(self):
        self.controller = ControllerClient(ElementType.CLIENT)
        self.controller.connect_to_configuration_server()
        self.controller.set_state(ElementState.RUNNING)
        self.remote_configurations = self.controller.get_servers_configuration()
        self.keras_model = self.controller.download_model()
        input_dimension = tuple(self.keras_model.layers[1].input_shape[1:3])
        self.datagen = ImageWithNames('./images_source/', ImageDataGenerator(), batch_size=16,
                                      target_size=input_dimension, interpolation="nearest")

    def send_log(self, message):
        self.controller.send_log(message)

    def get_server_from_configuration(self, type: ElementType):
        for server_config in self.remote_configurations:
            if type == server_config.type:
                return server_config

    def run(self):
        i = 0
        while (self.controller.get_state() == ElementState.RUNNING):
            data_batch, filenames = next(self.datagen)

            start = time.time()
            predicted = self.keras_model.predict(data_batch)
            end = time.time()
            self.send_log(str(end-start))
            print(predicted.shape)
            print(filenames)
            i += 1
            if (i == 10):
                exit()
            # send the picture to the server
            # send log with the perfomance done

        if self.controller.current_state == ElementState.RESET:
            # log connected to cloud server XXX
            # disconnect from cloud server
            self.configure_model_and_cloud()
        if self.controller.current_state == ElementState.STOP:
            # log disconnected
            self.controller.disconnect_to_configuration_server()

    def configure_model_and_cloud(self):
        self.remote_configurations = self.controller.get_servers_configuration()
        self.keras_model = self.controller.download_model()
        input_dimension = tuple(self.keras_model.layers[1].input_shape[1:])
        self.datagen = ImageWithNames('./images_source/', ImageDataGenerator(), batch_size=16,
                                      target_size=input_dimension, interpolation="nearest")
        # log model features maybe with a particular method that store the data in fashion way
        # self.cloud_interface = self.connect_to_cloud()
        # log connected to cloud server XXX
        print(input_dimension)

#    def connect_to_cloud_server(self):



class ImageWithNames(DirectoryIterator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filenames_np = np.array(self.filepaths)
        self.class_mode = None  # so that we only get the images back

    def _get_batches_of_transformed_samples(self, index_array):
        return (super()._get_batches_of_transformed_samples(index_array),
                self.filenames_np[index_array])


if __name__ == '__main__':
    client = MobileDevice()
    client.send_log("ciao")
    client.run()
