from thrift.protocol import TBinaryProtocol
from thrift.transport import TSocket, TTransport
from interfaces import ControllerInterface, ttypes
import tensorflow as tf

class ControllerClient:
    def __init__(self, conf_server_ip='localhost', port=10100):
        self.transport = TSocket.TSocket(conf_server_ip, port)
        self.transport = TTransport.TBufferedTransport(self.transport)
        self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
        self.server_interface = ControllerInterface.Client(self.protocol)
        self.current_state = None

    def connect_to_configuration_server(self):
        self.transport.open()

    def disconnect_to_configuration_server(self):
        self.transport.close()

    def register_and_get_configuration(self, name="client"):
        return
        #TODO

    def get_state(self):
        self.current_state = self.server_interface.get_state()

    def download_model(self):
        batch_dimension = 100000 #100 KB
        current_position = 0
        remaining = 1
        writer = open("./client.h5", "wb")

        while remaining:
            file_chunk = self.server_interface.get_model_chunk(ttypes.ServerType.CLIENT,
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

