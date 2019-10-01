from utils.surgeon import Surgeon
from utils.model_factory import ModelFactory
from interfaces import NeuralInterface
from interfaces import ttypes
from utils.thrift_servers import Server, ServerType


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
        del self.model_configuration
        del self.model

#TODO
#    NNLayer make_prediction(1: NNLayer data)


if __name__ == '__main__':
    service = NeuralInterfaceService()
    print("Starting python server...")
    processor = NeuralInterface.Processor(service)
    server = Server(ServerType.SIMPLE, processor, port=30300)
    server.serve()
    print("done!")