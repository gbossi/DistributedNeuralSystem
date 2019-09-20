from hospital.surgeon import Surgeon
from hospital.model_factory import ModelFactory
from thrift.transport import TSocket, TTransport
from thrift.protocol import TBinaryProtocol
from interfaces import NeuralInterface, ttypes
import logging


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

    def connect_to_computational_server(self):
        self.transportCS.close()

    def apply_configuration(self, model_name: str, split_layer: int):
        if not self.server_interface.exist_model():
            logging.warning("Apply mobile edge configuration to the server")
            self.server_interface.set_model(ttypes.ModelConfiguration(model_name, split_layer))
            client_model, _ = Surgeon().split(ModelFactory().get_new_model(model_name), split_layer)
        else:
            logging.warning("Apply server configuration to the mobile edge")
            current_config = self.server_interface.get_configuration()
            client_model, _ = Surgeon().split(ModelFactory().get_new_model(current_config.model_name),
                                              current_config.split_layer)

    def start_combined_prediction(self):
        ##TODO
        return


if __name__ == '__main__':
    # Maybe its better to get the argument from a config file
    # and pass the config file to the function as arg

    model_name = "VGG19"
    split_layer = 5

    client = MobileEdge()
    client.connect()
    client.apply_configuration(model_name, split_layer)
