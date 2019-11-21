from thrift.protocol import TBinaryProtocol, TMultiplexedProtocol
from thrift.transport import TSocket, TTransport
from interfaces import ControllerInterface, LogInterface
from interfaces.ttypes import ElementType, ElementState, ElementConfiguration, Message, SpecsMessage
import time
import subprocess

IP_MASTER_SERVER = 'localhost'
PORT_MASTER_SERVER = 10100


class MasterController:
    def __init__(self, server_ip='localhost', port=10100):
        self.socket = TSocket.TSocket(server_ip, port)
        self.transport = TTransport.TBufferedTransport(self.socket)
        self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
        self.con_proto = TMultiplexedProtocol.TMultiplexedProtocol(self.protocol, "Controller")
        self.log_proto = TMultiplexedProtocol.TMultiplexedProtocol(self.protocol, "Logger")
        self.controller_interface = ControllerInterface.Client(self.con_proto)
        self.logger_interface = LogInterface.Client(self.log_proto)
        self.element_type = None
        self.element_id = None
        self.current_state = ElementState.WAITING
        self.transport.open()

    def disconnect_to_configuration_server(self):
        self.transport.close()

    def register_element(self, element_type: ElementType, server_ip="localhost", server_port=0):
        """
        This function register a new element in the element table of the master server
        and publish on the logger a summary of the installed hardware, in this way
        the local controller acquire a valid element id.

        :param element_type: type of the element
        :param server_ip: address of the client to be registered
        :param server_port: port of the client to be registered
        :return: null
        """
        self.element_type = element_type
        local_config = {
            ElementType.CLOUD: ElementConfiguration(type=self.element_type, ip=server_ip, port=server_port),
            ElementType.CLIENT: ElementConfiguration(type=self.element_type),
            ElementType.CONTROLLER: ElementConfiguration(type=self.element_type)
        }[self.element_type]

        self.element_id = self.controller_interface.register_element(local_config)
        self.parse_and_send_specs()

    def parse_and_send_specs(self):
        command = subprocess.run(['lshw', '-short'], stdout=subprocess.PIPE)
        message_list = command.stdout.decode().split('\n')
        if command.returncode == 0:
            for i in range(2, len(message_list)):
                line = list(filter(None, message_list[i].split('  ')))
                line = [i for i in line if not i.startswith('/')]
                line = ' '.join(line)
                line = line.lstrip(' ')
                line = line.split()
                if len(line) > 2:
                    self.logger_interface.log_specs_message(SpecsMessage(time.time(), self.element_id,
                                                                         self.element_type, str(line[0]),
                                                                         str(' '.join(line[1:]))))
        command = subprocess.run(['lsb_release', '-a'], stdout=subprocess.PIPE)
        message_list = command.stdout.decode().split('\n')
        if command.returncode == 0:
            for i in range(1, len(message_list)):
                line = list(filter(None, message_list[i].split('\t')))
                if len(line) > 1:
                    self.logger_interface.log_specs_message(SpecsMessage(time.time(), self.element_id,
                                                                         self.element_type, str(line[0]),
                                                                         str(' '.join(line[1:]))))

    def send_log(self, message: str):
        self.logger_interface.log_message(Message(time.time(), self.element_id, self.element_type, message))