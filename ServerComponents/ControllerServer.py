from utils.model_factory import ModelFactory
from utils.surgeon import Surgeon
from utils.thrift_servers import Server, ServerType
from interfaces import ControllerInterface, ttypes
import os


class ControllerInterfaceService:
    def __init__(self):
        log_server = ttypes.ServerConfiguration(ip="localhost", port=20200, type=ttypes.ServerType.LOGGER)
        sink_server = ttypes.ServerConfiguration(ip="localhost", port=30300, type=ttypes.ServerType.SINK)
        self.device_model_path = "../models/client/"
        self.server_model_path = "../models/server/"
        self.model_state = ttypes.ModelState.UNSET
        self.instantiate_model(ttypes.ModelConfiguration("VGG16",5))

    def instantiate_model(self, model_configuration: ttypes.ModelConfiguration):
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

        self.model_state = ttypes.ModelState.AVAILABLE

    def get_state(self):
        return ttypes.ClientState.RUNNING

    def get_model_chunk(self, server_type: ttypes.ServerType, offset: int, size: int):

        reader = {ttypes.ServerType.CLIENT: open(self.device_model_path, "rb"),
                  ttypes.ServerType.SINK: open(self.server_model_path, "rb")
                  }[server_type]

        reader.seek(offset)
        data = reader.read(size)
        current_position = reader.tell()
        reader.seek(0, 2)

        return ttypes.FileChunk(data, remaining=reader.tell()-current_position)



if __name__ == '__main__':
    service = ControllerInterfaceService()
    print("Starting python server...")
    processor = ControllerInterface.Processor(service)
    server = Server(ServerType.THREADED, processor, port=10100)

    server.serve()
    print("done!")