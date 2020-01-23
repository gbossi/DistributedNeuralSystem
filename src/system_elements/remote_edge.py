import time
import numpy as np
import os
import uuid
import tensorflow as tf

from itertools import cycle
from keras_preprocessing.image import ImageDataGenerator, DirectoryIterator
from pathlib import Path
from src.components.client_components.sink_client import SinkClient
from src.components.client_components.internal_controller import InternalController
from thrift_interfaces.ttypes import ElementType, ElementState

BATCH_SIZE = 8
NO_IMAGES = 1000


class RemoteEdge:
    def __init__(self, master_ip, port):
        self.no_images = NO_IMAGES
        self.batch_size = BATCH_SIZE
        os.environ['IP_MASTER'] = master_ip
        self.controller = InternalController(server_ip=master_ip, port=port)
        self.controller.register_element(ElementType.CLIENT)
        self.sink_client = None
        self.test = None
        self.edge_model = None

    def run(self, images_source):
        datagen = DataGenerator(images_source,
                                ImageDataGenerator(),
                                batch_size=self.batch_size,
                                target_size=tuple(self.edge_model.layers[1].input_shape[1:3]),
                                interpolation="nearest")

        if self.test.is_test:
            self.run_test(datagen)
        else:
            self.run_edge(datagen)

        if self.controller.current_state == ElementState.READY:
            self.controller.wait_in_ready_state()

        if self.controller.current_state == ElementState.RUNNING:
            self.controller.send_log("Starting a new test with same configuration")

        if self.controller.current_state == ElementState.RESET:
            self.controller.send_log("Waiting a new model from master server")

        if self.controller.current_state == ElementState.STOP:
            self.controller.send_log("Shutting down the mobile device")

        return self.controller.current_state

    def run_test(self, datagen):
        images_read = 0
        self.controller.send_log("Starting a new test")

        while self.controller.update_state() == ElementState.RUNNING:
            data_batch, filenames = next(datagen)
            filenames = self.unique_filenames(filenames)
            start = time.time()
            predicted = self.edge_model.predict(data_batch)
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
            filenames = self.unique_filenames(filenames)
            start = time.time()
            predicted = self.edge_model.predict(data_batch)
            end = time.time()
            self.sink_client.put_partial_result(filenames, predicted)
            self.controller.log_performance_message_and_shape(self.batch_size, images_ids=filenames,
                                                              elapsed_time=end-start, shape=predicted.shape)

    def reset_values(self):
        self.controller.set_state(ElementState.WAITING)
        model_filename = self.controller.download_model()
        tf.keras.backend.clear_session()
        self.edge_model = tf.keras.models.load_model(model_filename)
        cloud_servers = self.controller.get_element_type_from_configuration(self.controller.get_servers_configuration(),
                                                                            ElementType.CLOUD)
        self.connect_to_sibling_cloud_server(cloud_servers)
        self.test = self.controller.get_test()
        if self.test.is_test:
            self.batch_size = self.test.edge_batch_size
            self.no_images = self.test.number_of_images

    def connect_to_sibling_cloud_server(self, cloud_servers):
        for cloud_server in cycle(cloud_servers):
            self.sink_client = SinkClient(cloud_server.ip, cloud_server.port)
            self.sink_client.connect_to_sink_service()
            if self.sink_client.register_to_sink(self.controller.model_id):
                return
            else:
                self.sink_client.disconnect_from_sink_service()

    def unique_filenames(self, filenames):
        clean_names = []
        for file in filenames:
            clean_names = clean_names+[uuid.uuid4().hex+"-"+Path(file).name]
        return clean_names


class DataGenerator(DirectoryIterator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filenames_np = np.array(self.filenames)
        self.class_mode = None

    def _get_batches_of_transformed_samples(self, index_array):
        return (super()._get_batches_of_transformed_samples(index_array),
                self.filenames_np[index_array])


def remote_edge_main(master_ip, master_port, images_source='./images_source/'):
    client = RemoteEdge(master_ip, master_port)
    client.reset_values()
    result = ElementState.RUNNING
    while result != ElementState.STOP:
        result = client.run(images_source)
        if result == ElementState.RESET:
            client.reset_values()


if __name__ == '__main__':
    remote_edge_main("localhost", 10100)
