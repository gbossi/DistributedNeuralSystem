from utils.model_factory import ModelFactory
from utils.surgeon import Surgeon
from utils.thrift_servers import Server, ServerType
from interfaces import ControllerInterface
from interfaces.ttypes import ElementType, ModelState, ModelConfiguration, ElementConfiguration, ElementState, FileChunk
import os


class ControllerInterfaceService:
    def __init__(self):
        #The following two lines should be done by the register element function
        log_server = ElementConfiguration(ip="localhost", port=20200, type=ElementType.LOGGER)
        sink_server = ElementConfiguration(ip="localhost", port=30300, type=ElementType.SINK)
        self.device_model_path = "../models/client/"
        self.server_model_path = "../models/server/"
        self.model_state = ModelState.UNSET
        # The following line should be made by external controller
        self.instantiate_model(ModelConfiguration("VGG16", 5))

    def instantiate_model(self, model_configuration: ModelConfiguration):
        device_model, server_model = Surgeon().split(
            ModelFactory().get_new_model(model_configuration.model_name),
            model_configuration.split_layer)

        if not os.path.exists(self.device_model_path):
            os.mkdir(self.device_model_path)
        elif not os.path.exists(self.server_model_path):
            os.mkdir(self.server_model_path)

        self.device_model_path = self.device_model_path+device_model.name+".h5"
        device_model.save(self.device_model_path)

        self.server_model_path = self.server_model_path+server_model.name+".h5"
        server_model.save(self.server_model_path)

        self.model_state = ModelState.AVAILABLE

    def get_state(self):
        return ElementState.WAITING

    def get_model_chunk(self, server_type: ElementType, offset: int, size: int):
        """
        Function used to download the partial neural network model by the
        clients and the computational server, depending on the type it will
        return a different model
        """

        reader = {ElementType.CLIENT: open(self.device_model_path, "rb"),
                  ElementType.SINK: open(self.server_model_path, "rb")
                  }[server_type]

        reader.seek(offset)
        data = reader.read(size)
        current_position = reader.tell()
        reader.seek(0, 2)

        return FileChunk(data, remaining=reader.tell()-current_position)



if __name__ == '__main__':
    service = ControllerInterfaceService()
    print("Starting python server...")
    processor = ControllerInterface.Processor(service)
    server = Server(ServerType.THREADED, processor, port=10100)
    server.serve()
