import time
import os

from thrift.protocol import TBinaryProtocol
from thrift.transport import TSocket, TTransport
from interfaces import SinkInterface
from interfaces.ttypes import Image


class SinkClient:
    def __init__(self, ip_address, port):
        self.transport = TSocket.TSocket(ip_address, port)
        self.buffered_transport = TTransport.TBufferedTransport(self.transport)
        self.protocol = TBinaryProtocol.TBinaryProtocol(self.buffered_transport)
        self.server_interface = SinkInterface.Client(self.protocol)

    def connect_to_sink_service(self):
        num_retries = 5
        for attempt_no in range(num_retries):
            try:
                self.buffered_transport.open()
                return
            except TTransport.TTransportException:
                print("Error: Cloud Server is not available \nFailed connection: "+str(attempt_no+1)
                      +" out of "+str(num_retries)+" attempts")
                if attempt_no < (num_retries-1):
                    time.sleep(1)
                else:
                    print("Last Attempt - Checking remote computing server on the master server")
                    self.transport = TSocket.TSocket(os.environ.get('IP_MASTER', 'Not Set'), self.transport.port)
                    self.buffered_transport = TTransport.TBufferedTransport(self.transport)
                    self.protocol = TBinaryProtocol.TBinaryProtocol(self.buffered_transport)
                    self.server_interface = SinkInterface.Client(self.protocol)
                    try:
                        self.buffered_transport.open()
                        return
                    except TTransport.TTransportException as error:
                        raise error

    def disconnect_from_sink_service(self):
        self.buffered_transport.close()

    def put_partial_result(self, image_ids, prediction):
        data = Image(image_ids, prediction.tobytes(), prediction.dtype.name, prediction.shape)
        self.server_interface.put_partial_result(data)

    def register_to_sink(self, model_id):
        #todo improve the connect to sink function, maybe using a list of available sinks
        time.sleep(2)
        success = self.server_interface.add_client(model_id)
        while not success:
            time.sleep(3)
            success = self.server_interface.add_client(model_id)
        return

