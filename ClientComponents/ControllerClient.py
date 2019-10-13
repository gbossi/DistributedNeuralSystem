from thrift.protocol import TBinaryProtocol, TMultiplexedProtocol
from thrift.transport import TSocket,TTransport
from interfaces import ControllerInterface, LogInterface
from interfaces.ttypes import ElementType, ElementState, ElementConfiguration, Message
import tensorflow as tf
import time

# Initial synchronizing time expressed in seconds
WAITING_TIME = 5


class ControllerClient:
    def __init__(self, element_type: ElementType, server_ip='localhost', port=10100):
        self.socket = TSocket.TSocket(server_ip, port)
        self.transport = TTransport.TBufferedTransport(self.socket)
        self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)

        self.con_proto = TMultiplexedProtocol.TMultiplexedProtocol(self.protocol, "Controller")
        self.log_proto = TMultiplexedProtocol.TMultiplexedProtocol(self.protocol, "Logger")

        self.controller_interface = ControllerInterface.Client(self.con_proto)
        self.logger_interface = LogInterface.Client(self.log_proto)
        self.element_type = element_type
        self.element_id = None
        self.current_state = ElementState.WAITING

    def connect_to_configuration_server(self):
        self.transport.open()
        self.register_controller()

    def disconnect_to_configuration_server(self):
        #final operation to be done
        self.transport.close()

    def register_controller(self, server_ip="localhost", server_port=0):
        local_config = {
            ElementType.LOGGER: ElementConfiguration(type=self.element_type, ip=server_ip, port=server_port),
            ElementType.CLOUD: ElementConfiguration(type=self.element_type, ip=server_ip, port=server_port),
            ElementType.CLIENT: ElementConfiguration(type=self.element_type)
        }[self.element_type]

        self.element_id = self.controller_interface.register_element(local_config)

    def get_servers_configuration(self):
        while self.current_state == ElementState.WAITING:
            time.sleep(WAITING_TIME)
            self.controller_interface.get_state(self.element_id)

        return self.controller_interface.get_new_configuration()

    def get_state(self):
        self.current_state = self.controller_interface.get_state(self.element_id)

    def set_state(self, element_state: ElementState):
        self.current_state = self.controller_interface.set_state(self.element_id, element_state)
        return True

    def download_model(self):
        batch_dimension = 100000  # 100 KB
        current_position = 0
        remaining = 1
        writer = open("./client.h5", "wb")

        while remaining:
            file_chunk = self.controller_interface.get_model_chunk(self.element_type,
                                                                   current_position, batch_dimension)
            current_position += batch_dimension
            remaining = file_chunk.remaining
            if batch_dimension < remaining:
                batch_dimension = remaining
            writer.write(file_chunk.data)

        return tf.keras.models.load_model("./client.h5")

    def send_log(self, message: str):
        self.logger_interface.log_message(Message(self.element_id, self.element_type, message))
