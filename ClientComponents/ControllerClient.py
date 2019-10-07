from thrift.protocol import TBinaryProtocol
from thrift.transport import TSocket, TTransport
from interfaces import ControllerInterface
from interfaces.ttypes import ElementType, ElementState, ElementConfiguration
import tensorflow as tf
import time

#Initial synchronizing time expressed in seconds
WAITING_TIME = 5

class ControllerClient:
    def __init__(self, element_type: ElementType, conf_server_ip='localhost', port=10100):
        self.transport = TSocket.TSocket(conf_server_ip, port)
        self.transport = TTransport.TBufferedTransport(self.transport)
        self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
        self.server_interface = ControllerInterface.Client(self.protocol)
        self.element_type = element_type
        self.id = None
        self.current_state = ElementState.WAITING

    def connect_to_configuration_server(self):
        self.transport.open()

    def disconnect_to_configuration_server(self):
        self.transport.close()

    def register_and_get_configuration(self, server_ip="localhost", server_port=0):
        local_config = {
            ElementType.LOGGER:  ElementConfiguration(type=self.element_type, ip=server_ip, port=server_port),
            ElementType.CLOUD: ElementConfiguration(type=self.element_type, ip=server_ip, port=server_port),
            ElementType.SINK: ElementConfiguration(type=self.element_type, ip=server_ip, port=server_port),
            ElementType.CLIENT: ElementConfiguration(type=self.element_type)
        }[self.element_type]

        self.id = self.server_interface.register_element(local_config)

        while self.current_state == ElementState.WAITING:
            time.sleep(WAITING_TIME)
            self.server_interface.get_state(self.id)

        return self.server_interface.get_new_configuration()


    def get_state(self):
        self.current_state = self.server_interface.get_state(self.id)
        return self.current_state

    def download_model(self):
        batch_dimension = 100000 #100 KB
        current_position = 0
        remaining = 1
        writer = open("./client.h5", "wb")

        while remaining:
            file_chunk = self.server_interface.get_model_chunk(self.element_type,
                                                               current_position, batch_dimension)
            current_position += batch_dimension
            remaining = file_chunk.remaining
            if batch_dimension < remaining:
                batch_dimension = remaining
            writer.write(file_chunk.data)

        return tf.keras.models.load_model("./client.h5")


if __name__ == '__main__':
    client = ControllerClient()
    client.connect_to_configuration_server()
    model = client.download_model()
    model.summary()

