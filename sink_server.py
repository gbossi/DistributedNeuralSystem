from thrift_servers import ServerType, Server
from interfaces import SinkInterface, ttypes
import queue
import numpy as np


# BUTTACI DENTRO ID DELLE FOTO
class SinkInterfaceService:
    def __init__(self):
        self.queue = queue.Queue()
        self.data_shape = None

    def is_empty(self):
        return self.queue.empty()

    def is_full(self):
        return self.queue.full()

    def put_partial_result(self, image_tuple):
        image_data = np.frombuffer(image_tuple.arr_bytes, dtype=image_tuple.data_type).reshape(
            image_tuple.shape)

        if len(image_data.shape == 4):
            self.check_shape(image_tuple.shape[1:3])
            for single_image in image_data:
                self.queue.put(single_image)
        elif len(image_data.shape == 3):
            self.check_shape(image_tuple.shape)
            self.queue.put(image_data)

    def check_shape(self, image_shape):
        if not self.data_shape:
            self.data_shape = image_shape
        elif self.data_shape != image_shape:
            raise AttributeError("Input Error, Unhandled Batch Dimension")

    def get_partial_result(self, batch_dim):
        batch_features = np.zeros([batch_dim]+list(self.data_shape))
        for i in range(batch_dim):
            batch_features[i] = self.queue.get()

        return ttypes.Image()


if __name__ == '__main__':
    service = SinkInterfaceService()
    print("Starting python server...")
    processor = SinkInterface.Processor(service)
    server = Server(ServerType.SIMPLE, processor, port=50500)
    server.serve()
    print("done!")
