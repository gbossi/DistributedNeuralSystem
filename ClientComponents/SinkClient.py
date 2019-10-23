from thrift.protocol import TBinaryProtocol
from thrift.transport import TSocket, TTransport
from interfaces import SinkInterface
from interfaces.ttypes import Image

class SinkClient:
    def __init__(self, ip_address="localhost", port=60600):
        self.transport = TSocket.TSocket(ip_address, port)
        self.transport = TTransport.TBufferedTransport(self.transport)
        self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
        self.server_interface = SinkInterface.Client(self.protocol)
        self._id_list = []

    def connect_to_sink_service(self):
        self.transport.open()

    def disconnect_from_sink_service(self):
        self.transport.close()

    def put_partial_result(self, image_ids, prediction):
        data = Image(image_ids, prediction.tobytes(), prediction.dtype.name, prediction.shape)
        self.server_interface.put_partial_result(data)
