import time
import os

from thrift.protocol import TBinaryProtocol
from thrift.transport import TSocket, TTransport
from thrift_interfaces import SinkInterface
from thrift_interfaces.ttypes import Image

NUM_RETRIES = 5
WAITING_TIME = 1

class SinkClient:
    def __init__(self, ip_address, port):
        self.transport = TSocket.TSocket(ip_address, port)
        self.buffered_transport = TTransport.TBufferedTransport(self.transport)
        self.protocol = TBinaryProtocol.TBinaryProtocol(self.buffered_transport)
        self.server_interface = SinkInterface.Client(self.protocol)

    def connect_to_sink_service(self):
        for attempt_no in range(NUM_RETRIES):
            try:
                self.buffered_transport.open()
                return
            except TTransport.TTransportException:
                print("Error: Cloud Server is not available \nFailed connection: "+str(attempt_no+1)
                      +" out of "+str(NUM_RETRIES)+" attempts")
                if attempt_no < (NUM_RETRIES-1):
                    time.sleep(WAITING_TIME)
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
        for attempt_no in range(NUM_RETRIES):
            success = self.server_interface.add_client(model_id)
            if success:
                print("Compatible Cloud Server found")
                return True
            else:
                print("Error: Cloud Server has a different or unset model \nFailed connection: "+str(attempt_no+1)
                  +" out of "+str(NUM_RETRIES)+" attempts")
                time.sleep(WAITING_TIME)
        print("Maximum attempt reached. Trying to connect to a new Cloud Server")
        return False

