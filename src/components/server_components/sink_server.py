import numpy as np
from queue import Queue
from thrift_interfaces.ttypes import Image


class SinkInterfaceService:
    def __init__(self):
        self.model_id =None
        self.queue = Queue()
        self.data_shape = None
        self.client_connected = 0

    def put_partial_result(self, image_tuple):
        image_data = np.frombuffer(image_tuple.arr_bytes, dtype=image_tuple.data_type).reshape(image_tuple.shape)
        image_id = image_tuple.id
        number_of_images = len(image_data)
        if self.check_shape(image_tuple.shape[1:]):
            for i in range(number_of_images):
                self.queue.put((image_id[i], image_data[i]))

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
        return id_list, batch_features

    def check_shape(self, image_shape):
        if self.data_shape is None:
            self.data_shape = image_shape
            return True
        elif self.data_shape == image_shape:
            return True
        else:
            print("Input Error, Unhandled Image Dimension "+str(self.data_shape)+"!="+str(image_shape)+" skipping input")
            return False

    def add_client(self, ext_model_id):
        print(self.model_id)
        print(ext_model_id)
        if self.model_id is None or ext_model_id is None or ext_model_id != self.model_id:
            return False
        else:
            self.client_connected += 1
            return True

    def reset_sink(self, model_id):
        self.data_shape = None
        self.client_connected = 0
        self.model_id = model_id
