from hospital.surgeon import Surgeon
from hospital.model_factory import ModelFactory
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from interfaces import NeuralInterface
from interfaces import ttypes
import numpy as np


class NeuralInterfaceService:
    def __init__(self):
        self.model_configuration = None
        self.model = None

    def set_model(self, model_configuration):
        self.model_configuration = model_configuration
        _, self.model = Surgeon().split(ModelFactory().get_new_model(model_configuration.model_name),
                                        model_configuration.split_layer)

    def exist_model(self):
        if not self.model_configuration:
            return False
        else:
            return True

    def get_configuration(self):
        return ttypes.ModelConfiguration(self.model_configuration.model_name,
                                         self.model_configuration.split_layer)

    def uninstantiate_model(self):
        del self.config
        del self.model

#TODO
#    NNLayer make_prediction(1: NNLayer data)


class Server:
    def __init__(self, service, port=9090):
        self.processor = NeuralInterface.Processor(service)
        self.transport = TSocket.TServerSocket(port=port)
        self.tfactory = TTransport.TBufferedTransportFactory()
        self.pfactory = TBinaryProtocol.TBinaryProtocolFactory()
        # This is single thread server
        # TODO something better Threaded Server !!!
        # even better maybe to let somebody decide which kind of server depending on the
        # service
        self.server = TServer.TSimpleServer(self.processor, self.transport, self.tfactory, self.pfactory)

    def serve(self):
        self.server.serve()


if __name__ == '__main__':
    service = NeuralInterfaceService()
    print("Starting python server...")
    server = Server(service, port=30300)
    server.serve()
    print("done!")