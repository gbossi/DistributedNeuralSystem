from thrift.protocol import TBinaryProtocol
from thrift.transport import TSocket, TTransport
from interfaces import SinkInterface, ttypes

class SinkClient:
    def __init__(self, ip_address="localhost", port=60600):
        self.transportS = TSocket.TSocket(ip_address, port)
        self.transportS = TTransport.TBufferedTransport(self.transportS)
        self.protocolS = TBinaryProtocol.TBinaryProtocol(self.transportS)
        self.server_interfaceS = SinkInterface.Client(self.protocolS)
        self._id_list = []

    def connect_to_sink_service(self):
        self.transportS.open()

    def send_prediction(self, image_ids, prediction):
        data = ttypes.Image(image_ids, prediction.tobytes(), prediction.dtype.name, prediction.shape, False)
        self.server_interfaceS.put_partial_result(data)
