from utils.model_factory import ModelFactory
from utils.surgeon import Surgeon
from utils.thrift_servers import Server, ServerType
from interfaces import ControllerInterface
from interfaces.ttypes import  Configuration, ElementConfiguration, ElementType, ElementState, FileChunk
from interfaces.ttypes import ModelState, ModelConfiguration
import os, uuid


class ElementTable:
    def __init__(self):
        self.element_dict = {}

    def insert(self, element_id, element_type, element_ip='unavailable', element_port=0,
               element_state=ElementState.WAITING):
        self.element_dict.update({element_id:
                                      {"type": element_type, "ip": element_ip, "port": element_port,
                                       "state": element_state}})
        if self.get_element_state(element_id is not ElementState.RUNNING):
            self.trigger_state()


    def trigger_state(self):
        if self.exist_not_running_type(ElementType.CONTROLLER):
            self.update_state_by_type(ElementType.CONTROLLER, ElementState.RUNNING)
        if self.exist_not_running_type(ElementType.LOGGER):
            self.update_state_by_type(ElementType.LOGGER, ElementState.RUNNING)
            if self.exist_not_running_type(ElementType.SINK):
                self.update_state_by_type(ElementType.SINK, ElementState.RUNNING)
                if self.exist_not_running_type(ElementType.CLOUD):
                    self.update_state_by_type(ElementType.CLOUD, ElementState.RUNNING)
                    if self.exist_not_running_type(ElementType.CLIENT):
                        self.update_state_by_type(ElementType.CLIENT, ElementState.RUNNING)

    def get_server_configuration(self):
        server_configurations = []
        for element in [x for x in self.element_dict.values() if x['type'] != ElementType.CLIENT]:
            server_configurations.append(ElementConfiguration(element['type'], element['ip'], element['port']))
        return server_configurations

    def get_element_state(self, id):
        return self.element_dict.get(id)['state']

    def exist_not_running_type(self, type: ElementType):
        if len([x for x in self.element_dict.values() if x['type'] == type and x['state'] is ElementState.RUNNING]) != 0:
            return True
        else:
            return False

    def update_state_by_type(self, type: ElementType, state: ElementState):
        for element in self.element_dict.items():
            if element[1]['type'] is type:
                self.element_dict[element[0]]['state'] = state


class ControllerInterfaceService:
    def __init__(self):
        # The following two lines should be done by the register element function
        log_server = ElementConfiguration(ip="localhost", port=20200, type=ElementType.LOGGER)
        sink_server = ElementConfiguration(ip="localhost", port=30300, type=ElementType.SINK)
        self.device_model_path = "../models/client/"
        self.server_model_path = "../models/server/"
        self.model_state = ModelState.UNSET
        self.element_table = ElementTable()
        # TODO even the following line has to be modified
        # The following line should be made by external controller
        self.model_configuration = ModelConfiguration("VGG16", 5)
        self.instantiate_model(model_configuration=self.model_configuration)

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

    def get_state(self, element_id):
        return self.element_table.get_element_state(element_id)

    def register_element(self, local_config: ElementConfiguration):
        element_id = str(uuid.uuid4().hex)
        if local_config.type is not ElementType.CLIENT:
            self.element_table.insert(element_id, local_config.type, local_config.ip, local_config.port)
        else:
            self.element_table.insert(element_id, local_config.type)
        return element_id

    def get_new_configuration(self):
        return Configuration(self.element_table.get_server_configuration())

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
    id = service.register_element(
        ElementConfiguration(ElementType.CONTROLLER, ip='localhost', port=10100))
    to_print = service.get_new_configuration()
    print(to_print)

    print("Starting python server...")
    processor = ControllerInterface.Processor(service)
    server = Server(ServerType.THREADED, processor, port=10100)

