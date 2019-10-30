from thrift.protocol import TBinaryProtocol, TMultiplexedProtocol
from thrift.transport import TSocket, TTransport
from interfaces import ControllerInterface, LogInterface
from interfaces.ttypes import ElementType, ElementState, ElementConfiguration, Message
import time
import subprocess

IP_MASTER_SERVER = 'localhost'
PORT_MASTER_SERVER = 10100


class MasterController:
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

    def disconnect_to_configuration_server(self):
        self.transport.close()

    def register_controller(self, server_ip="localhost", server_port=0):
        """
        This function register a new element in the element table of the master server
        and publish on the logger a summary of the installed hardware, in this way
        the local controller acquire a valid element id.

        :param server_ip: address of the client to be registered
        :param server_port: port of the client to be registered
        :return: null
        """
        local_config = {
            ElementType.CLOUD: ElementConfiguration(type=self.element_type, ip=server_ip, port=server_port),
            ElementType.CLIENT: ElementConfiguration(type=self.element_type),
            ElementType.CONTROLLER: ElementConfiguration(type=self.element_type)
        }[self.element_type]

        self.element_id = self.controller_interface.register_element(local_config)

        command = subprocess.run(['lshw', '-short'], stdout=subprocess.PIPE)
        message_list = command.stdout.decode().split('\n')
        if command.returncode == 0:
            for message in message_list:
                print(message)
        else:
            self.logger_interface.send_log_message("Unable to understand hardware specs")
        command = subprocess.run(['lsb_release', '-a'], stdout=subprocess.PIPE)
        if command.returncode == 0:
            pass
            # self.logger_interface.send_log_message(command.stdout.decode())
        else:
            self.logger_interface.send_log_message("Unable to understand installed OS")


    def send_log(self, message: str):
        self.logger_interface.log_message(Message(time.time(), self.element_id, self.element_type, message))
