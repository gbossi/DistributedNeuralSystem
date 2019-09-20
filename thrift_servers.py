from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer


class Server:
    def __init__(self, processor, port=9090):
        self.transport = TSocket.TServerSocket(port=port)
        self.tfactory = TTransport.TBufferedTransportFactory()
        self.pfactory = TBinaryProtocol.TBinaryProtocolFactory()
        # This is single thread server
        # TODO something better Threaded Server !!!
        # even better maybe to let somebody decide which kind of server depending on the
        # service
        self.server = TServer.TSimpleServer(processor, self.transport, self.tfactory, self.pfactory)

    def serve(self):
        self.server.serve()
