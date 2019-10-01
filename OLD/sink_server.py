from utils.thrift_servers import ServerType, Server
from interfaces import SinkInterface, ttypes
import queue
import numpy as np


class SinkInterfaceService:
    def __init__(self):
        self.queue = queue.Queue()
        self.data_shape = None

    def is_empty(self):
        return self.queue.empty()

    def is_full(self):
        return self.queue.full()

    def put_partial_result(self, image_tuple):
        image_data = np.frombuffer(image_tuple.arr_bytes, dtype=image_tuple.data_type).reshape(image_tuple.shape)
        image_id = image_tuple.id
        print(image_data.shape)
        self.check_shape(image_tuple.shape[1:3])
        for i in range(len(image_data)):
            self.queue.put((image_id[i], image_data[i]))
        self.correct_way()

    def correct_way(self):
        print(self.queue.qsize())


    def check_shape(self, image_shape):
        if not self.data_shape:
            self.data_shape = image_shape
        elif self.data_shape != image_shape:
            raise AttributeError("Input Error, Unhandled Batch Dimension")

    def get_partial_result(self, batch_dim):
        id_list = []
        batch_features = np.zeros([batch_dim]+list(self.data_shape))
        for i in range(batch_dim):
            element = self.queue.get()
            id_list.append(element[0])
            batch_features[i] = element[1]
        last = False

        return ttypes.Image(id_list, batch_features.tobytes(), batch_features.dtype.name, batch_features.shape, last)


if __name__ == '__main__':
    service = SinkInterfaceService()
    print("Starting python server...")
    processor = SinkInterface.Processor(service)
    server = Server(ServerType.THREADED, processor, port=60600)
    server.serve()
    print("done!")
