from hospital.surgeon import Surgeon
from hospital.model_factory import ModelFactory
from thrift.transport import TSocket, TTransport
from thrift.protocol import TBinaryProtocol
from interfaces import NeuralInterface, ImageLoader, ttypes
import logging, cv2
import numpy as np


class MobileEdge:
    def __init__(self, ip_addressCS="localhost", portCS=30300, ip_addressIL="localhost", portIL=40400):
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

    def input_generator(self, batch_dim=2, maximum=10):
        no_batch = 0

        while no_batch < maximum:
            no_batch += 1
            image_tuple = self.server_interfaceIL.get_image()

            input_dimension = tuple(self.client_model.layers[1].input_shape[1:])
            batch_features = np.zeros([batch_dim]+list(input_dimension))
            image_data = self.adapt_image_to_input_dimension(image_tuple, input_dimension)

            for i in range(batch_dim):
                batch_features[i] = image_data
                image_tuple = self.server_interfaceIL.get_image()
                image_data = self.adapt_image_to_input_dimension(image_tuple, input_dimension)
            yield batch_features

    def adapt_image_to_input_dimension(self, image_tuple, input_dimension):
        image_data = np.frombuffer(image_tuple.arr_bytes, dtype=image_tuple.data_type).reshape(
            image_tuple.shape)
        x_dim, y_dim, _ = input_dimension
        image_data = cv2.resize(image_data, (x_dim, y_dim), interpolation=cv2.INTER_AREA)
        return image_data

    def start_combined_prediction(self, n):
        prediction = self.client_model.predict_generator(self.input_generator(), steps=10)
        return prediction


if __name__ == '__main__':
    # Maybe its better to get the argument from a config file
    # and pass the config file to the function as arg

    model_name = "VGG19"
    split_layer = 5

    client = MobileEdge()
    client.connect_to_computational_server()
    client.apply_configuration(model_name, split_layer)
    client.connect_to_image_loader()
    print(client.start_combined_prediction(1))
