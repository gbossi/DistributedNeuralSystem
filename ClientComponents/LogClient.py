from thrift.protocol import TBinaryProtocol
from thrift.transport import TSocket, TTransport
from interfaces import LoggerInterface


class Logger:
    def __init__(self, conf_server_ip='localhost', port=10100):
        self.transport = TSocket.TSocket(conf_server_ip, port)
        self.transport = TTransport.TBufferedTransport(self.transport)
        self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
        self.server_interface = LoggerInterface.Client(self.protocol)

    def connect_to_logger_server(self):
        self.transport.open()

    def disconnect_to_logger_server(self):
        self.transport.close()

    def send_log(self, message):
        self.server_interface.log_message(message)
