import cv2
import logging
import operator

import numpy as np
from thrift.protocol import TBinaryProtocol
from thrift.transport import TSocket, TTransport

from hospital.model_factory import ModelFactory
from hospital.surgeon import Surgeon
from interfaces import NeuralInterface, ImageLoader, ttypes
from functools import reduce


class InputGenerator:
    def __init__(self, ip_address="localhost", port=40400):
        self.transportIL = TSocket.TSocket(ip_address, port)
        self.transportIL = TTransport.TBufferedTransport(self.transportIL)
        self.protocolIL = TBinaryProtocol.TBinaryProtocol(self.transportIL)
        self.server_interfaceIL = ImageLoader.Client(self.protocolIL)
        self.id_list = []

    def connect_to_image_loader(self):
        self.transportIL.open()

    def disconnect_from_image_loader(self):
        self.transportIL.close()

    def run(self, batch_dim, input_dimension):
        batch_features = np.zeros([batch_dim]+list(input_dimension))
        print(batch_features.shape)

        while True:
            for i in range(batch_dim):
                image_tuple = self.server_interfaceIL.get_image()
                image_data = self.adapt_image_to_model_dimension(image_tuple, input_dimension)
                batch_features[i] = image_data
                self.id_list.append(reduce(operator.add, image_tuple.id))
                if image_tuple.last:
                    break
            else:
                yield batch_features
                continue
            break

    def get_idlist(self):
        temp_list = self.id_list
        del self.id_list
        self.id_list = []
        return temp_list

    @staticmethod
    def adapt_image_to_model_dimension(image_tuple, input_dimension):
        image_data = np.frombuffer(image_tuple.arr_bytes, dtype=image_tuple.data_type).reshape(
            image_tuple.shape)
        image_data = cv2.resize(image_data, tuple(input_dimension[0:2]), interpolation=cv2.INTER_AREA)
        return image_data


class MobileEdge:
    def __init__(self, ip_address="localhost", port=30300):
        self.client_model = None
        self.transportCS = TSocket.TSocket(ip_address, port)
        self.transportCS = TTransport.TBufferedTransport(self.transportCS)
        self.protocolCS = TBinaryProtocol.TBinaryProtocol(self.transportCS)
        self.server_interfaceCS = NeuralInterface.Client(self.protocolCS)

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

    def start_combined_prediction(self, generator: InputGenerator):
        # Batch should be the maximum amount of data that could fit inside the memory
        # Steps means how many times
        model_dimension = self.client_model.layers[1].input_shape[1:]
        prediction = self.client_model.predict_generator(generator.run(batch_dim=1, input_dimension=model_dimension),
                                                         steps=1)
        self.send_prediction(generator.get_idlist())
        return prediction

    def send_prediction(self, prediction):
        print("Number of MB "+str(prediction.nbytes / 1000000))
        print(self.client_model.summary())
        return


if __name__ == '__main__':
    # Maybe its better to get the argument from a config file
    # and pass the config file to the function as arg

    model_name = "VGG19"
    split_layer = -1

    image_gen = InputGenerator()
    image_gen.connect_to_image_loader()

    client = MobileEdge()
    client.connect_to_computational_server()
    client.apply_configuration(model_name, split_layer)
    client.start_combined_prediction(image_gen)
