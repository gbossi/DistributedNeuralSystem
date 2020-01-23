import random
import time
import uuid
import numpy as np
import os

from itertools import cycle
from PIL import Image
from tflite_runtime.interpreter import Interpreter
from pathlib import Path
from src.components.client_components.sink_client import SinkClient
from src.components.client_components.internal_controller import InternalController
from thrift_interfaces.ttypes import ElementType, ElementState

BATCH_SIZE = 8
NO_IMAGES = 1000


class RemoteEdge:
    def __init__(self, master_ip, port):
        self.batch_size = BATCH_SIZE
        self.no_images = NO_IMAGES
        os.environ['IP_MASTER'] = master_ip
        self.controller = InternalController(server_ip=master_ip, port=port)
        self.controller.register_element(ElementType.CLIENT)
        self.sink_client = None
        self.interpreter = None
        self.test = None

    def run(self, images_source):
        datagen = DataGenerator(images_source,
                                batch_size=self.batch_size,
                                target_size=self.interpreter.get_input_details()[0]['shape'][1:3])

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
            data_batch, filenames = datagen.get_batch()
            filenames = self.clean_filenames(filenames)
            start = time.time()
            predicted = predict_batch(self.interpreter, data_batch)
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
            data_batch, filenames = datagen.get_batch()
            filenames = self.clean_filenames(filenames)
            start = time.time()
            predicted = predict_batch(self.interpreter, data_batch)
            end = time.time()
            self.sink_client.put_partial_result(filenames, predicted)
            self.controller.log_performance_message_and_shape(self.batch_size, images_ids=filenames,
                                                              elapsed_time=end-start, shape=predicted.shape)

    def reset_values(self):
        self.controller.set_state(ElementState.WAITING)
        model_filename = self.controller.download_model()
        self.interpreter = Interpreter(model_filename)
        self.interpreter.allocate_tensors()
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


def predict_batch(interpreter, data_batch):
    dimensions = [len(data_batch)] + list(interpreter.get_output_details()[-1]['shape'][1:])
    result = np.zeros(dimensions)
    for i in range(dimensions[0]):
        set_input_tensor(interpreter, data_batch[i])
        result[i] = classify_image(interpreter, data_batch[i])
    return result


def set_input_tensor(interpreter, image):
    tensor_index = interpreter.get_input_details()[0]['index']
    input_tensor = interpreter.tensor(tensor_index)()[0]
    input_tensor[:, :] = image


def classify_image(interpreter, image):
    """Returns a sorted array of classification results."""
    set_input_tensor(interpreter, image)
    interpreter.invoke()
    output_details = interpreter.get_output_details()[0]
    output = interpreter.get_tensor(output_details['index'])
    return output


class DataGenerator:
    def __init__(self, source: str, batch_size: int, target_size):
        self.filenames = self.retrieve_filenames(source)
        self.batch_size = batch_size
        self.target_size = target_size

    def get_batch(self):
        path_list = []
        data_batch = []
        for i in range(self.batch_size):
            path = random.choice(self.filenames)
            path_list = path_list+[path]
            image = Image.open(path).convert('RGB').resize(self.target_size, Image.NEAREST)
            data_batch = data_batch+[image]
        return data_batch, path_list

    @staticmethod
    def retrieve_filenames(source):
        dirlist = [item for item in os.listdir(source) if os.path.isdir(os.path.join(source, item))]
        filenames = []
        for directory in dirlist:
            subdir = os.path.join(source, directory)
            typedir = [item for item in os.listdir(subdir)]
            for exname in typedir:
                filenames = filenames+[os.path.join(subdir, exname)]
        return filenames


def remote_edge_lite_main(master_ip, master_port, images_source='./images_source/'):
    client = RemoteEdge(master_ip, master_port)
    client.reset_values()
    result = ElementState.RUNNING
    while result != ElementState.STOP:
        result = client.run(images_source)
        if result == ElementState.RESET:
            client.reset_values()


if __name__ == '__main__':
    remote_edge_lite_main("localhost", 10100)
