import cv2
import logging

import numpy as np
from thrift.protocol import TBinaryProtocol
from thrift.transport import TSocket, TTransport

from hospital.model_factory import ModelFactory
from hospital.surgeon import Surgeon
from interfaces import NeuralInterface, ImageLoader, ttypes


class MobileEdge:
    def __init__(self, ip_addressCS="localhost", portCS=30300, ip_addressIL="localhost", portIL=40400):
        self.client_model = None
        self.init_computation_server(ip_addressCS, portCS)
        self.init_image_loader(ip_addressIL, portIL)

    def init_computation_server(self, ip_address, port):
        self.transportCS = TSocket.TSocket(ip_address, port)
        self.transportCS = TTransport.TBufferedTransport(self.transportCS)
        self.protocolCS = TBinaryProtocol.TBinaryProtocol(self.transportCS)
        self.server_interfaceCS = NeuralInterface.Client(self.protocolCS)

    def init_image_loader(self, ip_address, port):
        self.transportIL = TSocket.TSocket(ip_address, port)
        self.transportIL = TTransport.TBufferedTransport(self.transportIL)
        self.protocolIL = TBinaryProtocol.TBinaryProtocol(self.transportIL)
        self.server_interfaceIL = ImageLoader.Client(self.protocolIL)

    def connect_to_image_loader(self):
        self.transportIL.open()

    def disconnect_from_image_loader(self):
        self.transportIL.close()

    def connect_to_computational_server(self):
        self.transportCS.open()

    def disconnect_from_computational_server(self):
        self.transportCS.close()

    def apply_configuration(self, model_name: str, split_layer: int):
        if not self.server_interfaceCS.exist_model():
            logging.warning("Apply mobile edge configuration to the server")
            self.server_interfaceCS.set_model(ttypes.ModelConfiguration(model_name, split_layer))
            self.client_model, _ = Surgeon().split(ModelFactory().get_new_model(model_name), split_layer)
        else:
            logging.warning("Apply server configuration to the mobile edge")
            current_config = self.server_interfaceCS.get_configuration()
            self.client_model, _ = Surgeon().split(ModelFactory().get_new_model(current_config.model_name),
                                              current_config.split_layer)

    def input_generator(self, batch_dim=2):
        input_dimension = self.client_model.layers[1].input_shape[1:]
        batch_features = np.zeros([batch_dim]+list(input_dimension))

        while True:
            for i in range(batch_dim):
                image_tuple = self.server_interfaceIL.get_image()
                image_data = self.adapt_image_to_model_dimension(image_tuple)
                batch_features[i] = image_data
                if image_tuple.last:
                    break
            else:
                yield batch_features
                continue
            break

    def adapt_image_to_model_dimension(self, image_tuple):
        model_dimension = tuple(self.client_model.layers[1].input_shape[1:3])
        image_data = np.frombuffer(image_tuple.arr_bytes, dtype=image_tuple.data_type).reshape(
            image_tuple.shape)
        image_data = cv2.resize(image_data, model_dimension, interpolation=cv2.INTER_AREA)
        return image_data

    def start_combined_prediction(self, n):
        # Batch should be the maximum amount of data that could fit inside the memory
        # Steps means how many times
        prediction = self.client_model.predict_generator(self.input_generator(batch_dim=1), steps=1)
        print("prediction done")
        print(prediction.shape)
        self.send_prediction(prediction)
        return prediction

    def send_prediction(self, prediction):
        print("Number of MB " + str(prediction.nbytes/1000000))
        print(self.client_model.summary())
        return


if __name__ == '__main__':
    # Maybe its better to get the argument from a config file
    # and pass the config file to the function as arg

    model_name = "VGG19"
    split_layer = -1

    client = MobileEdge()
    client.connect_to_computational_server()
    client.apply_configuration(model_name, split_layer)
    client.connect_to_image_loader()
    client.start_combined_prediction(3)
