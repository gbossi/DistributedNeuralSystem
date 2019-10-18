from queue import Queue
from interfaces.ttypes import Image
import numpy as np


class SinkInterfaceService:
    def __init__(self):
        self.queue = Queue()
        self.data_shape = None

    def put_partial_result(self, image_tuple):
        image_data = np.frombuffer(image_tuple.arr_bytes, dtype=image_tuple.data_type).reshape(image_tuple.shape)
        image_id = image_tuple.id
        number_of_images = len(image_data)
        if self.check_shape(image_tuple.shape[1:]):
            for i in range(number_of_images):
                self.queue.put((image_id[i], image_data[i]))
        print(self.queue.qsize())

    def get_remote_partial_result(self, batch_dim):
        id_list = []
        batch_features = np.zeros([batch_dim]+list(self.data_shape))
        for i in range(batch_dim):
            element = self.queue.get()
            id_list.append(element[0])
            batch_features[i] = element[1]
        return Image(id_list, batch_features.tobytes(), batch_features.dtype.name, batch_features.shape)

    def get_partial_result(self, batch_dim):
        id_list = []
        batch_features = np.zeros([batch_dim]+list(self.data_shape))
        for i in range(batch_dim):
            element = self.queue.get()
            id_list.append(element[0])
            batch_features[i] = element[1]
        print(self.queue.qsize())
        return id_list, batch_features

    def check_shape(self, image_shape):
        if self.data_shape is None:
            self.data_shape = image_shape
            return True
        elif self.data_shape == image_shape:
            return True
        else:
            print("Input Error, Unhandled Image Dimension, skipping input")
            return False

