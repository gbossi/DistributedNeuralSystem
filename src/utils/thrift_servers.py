from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer, TNonblockingServer
from enum import Enum
import socket


class ServerType(Enum):
    SIMPLE = "simple"
    THREADED = "threaded"
    POOL_THREADED = "poolThreaded"
    NON_BLOCKING = "nonBlocking"


class Server:
    def __init__(self, server_type, processor, port, no_threads=4):
        if not isinstance(server_type, ServerType):
            raise TypeError("Server type must be instance of ServerType")

        self.transport = TSocket.TServerSocket(port=port)
        self.tfactory = TTransport.TBufferedTransportFactory()
        self.pfactory = TBinaryProtocol.TBinaryProtocolFactory()

        self.port = port
        self.ip = socket.gethostbyname(socket.gethostname())

        self.server = {
            "simple": TServer.TSimpleServer(processor, self.transport, self.tfactory, self.pfactory),
            "threaded": TServer.TThreadedServer(processor, self.transport, self.tfactory, self.pfactory),
            "poolThreaded": TServer.TThreadPoolServer(processor, self.transport, self.tfactory, self.pfactory),
            "nonBlocking": TNonblockingServer.TNonblockingServer(processor, self.transport, self.tfactory,
                                                                 self.pfactory)
        }[server_type.value]

    def serve(self):
        self.server.serve()

    def stop(self):
        pass
