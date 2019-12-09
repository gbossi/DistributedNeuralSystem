import time

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

    def connect_to_sink_service(self):
        num_retries = 5
        for attempt_no in range(num_retries):
            try:
                self.transport.open()
                return
            except TTransport.TTransportException as error:
                if attempt_no < (num_retries-1):
                    print("Error: Cloud Server is not available \nFailed connection: "+str(attempt_no+1)
                          +" out of "+str(num_retries)+" attempts")
                    time.sleep(5)
                else:
                    raise error

    def disconnect_from_sink_service(self):
        self.transport.close()

    def put_partial_result(self, image_ids, prediction):
        data = Image(image_ids, prediction.tobytes(), prediction.dtype.name, prediction.shape)
        self.server_interface.put_partial_result(data)
