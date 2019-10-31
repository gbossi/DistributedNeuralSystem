from utils.model_factory import ModelFactory
from utils.surgeon import Surgeon
from utils.element_table import ElementTable
from interfaces.ttypes import Configuration, ElementConfiguration, ElementType, ElementState, FileChunk
from interfaces.ttypes import ModelState, ModelConfiguration
import os, uuid


class ControllerInterfaceService:
    def __init__(self):
        self.device_base_path = "./models/client/"
        self.server_base_path = "./models/server/"
        self.model_state = ModelState.UNSET
        self.element_table = ElementTable()

    # --------- MODEL HANDLING SECTION --------- #

    def instantiate_model(self, model_configuration: ModelConfiguration):
        """
        Given a configuration, this function initializes the model that
        the servers and the client will download

        :param model_configuration: A model name and a split layer
        :return: None
        """

        device_model, server_model = Surgeon().split(
            ModelFactory().get_new_model(model_configuration.model_name),
            model_configuration.split_layer)

        if not os.path.exists(self.device_base_path):
            os.mkdir(self.device_base_path)
        elif not os.path.exists(self.server_base_path):
            os.mkdir(self.server_base_path)

        self.device_model_path = self.device_base_path+device_model.name+".h5"
        device_model.save(self.device_model_path)

        self.server_model_path = self.server_base_path+server_model.name+".h5"
        server_model.save(self.server_model_path)

        self.model_state = ModelState.AVAILABLE

        return model_configuration

    def set_model_state(self, model_state: ModelState):
        self.model_state = model_state
        return model_state

    def is_model_available(self):
        if self.model_state != ModelState.AVAILABLE:
            return False
        else:
            return True

    def get_model_chunk(self, server_type: ElementType, offset: int, size: int):
        """
        Function used to download the partial neural network model by the
        clients and the computational server, depending on the type it will
        return a different model

        :param server_type: define the type of the model to be sent
        :param offset: define the offset
        :param size: define the size requested
        :return: a binary file chunk
        """

        reader = {ElementType.CLIENT: open(self.device_model_path, "rb"),
                  ElementType.CLOUD: open(self.server_model_path, "rb")
                  }[server_type]

        reader.seek(offset)
        data = reader.read(size)
        current_position = reader.tell()
        reader.seek(0, 2)

        return FileChunk(data, remaining=reader.tell()-current_position)

    # --------- ELEMENT HANDLING SECTION --------- #

    def register_element(self, local_config: ElementConfiguration):
        """
        When a new element of the distributed network connects to the controller service
        first it registers inside the element table

        :param local_config: register a local configuration
        :return: a unique id
        """

        element_id = str(uuid.uuid4().hex)
        if local_config.type is ElementType.CLOUD:
            self.element_table.insert(element_id, local_config.type, local_config.ip, local_config.port)
        elif local_config.type is ElementType.CLIENT:
            self.element_table.insert(element_id, local_config.type)
        elif local_config.type is ElementType.CONTROLLER:
            self.element_table.insert(element_id, local_config.type, element_state=ElementState.RUNNING)
        return element_id

    def trigger_state(self, element_id):
        if self.model_state is ModelState.AVAILABLE:
            if self.element_table.get_element_type(element_id) in [ElementType.CLIENT, ElementType.CLOUD]:
                if self.element_table.exist_type_in_state(ElementType.CLIENT, ElementState.WAITING):
                    if self.element_table.exist_type_in_state(ElementType.CLOUD, ElementState.RUNNING):
                        self.element_table.update_state_by_type(ElementType.CLIENT, ElementState.RUNNING)

    def get_state(self, element_id):
        self.trigger_state(element_id)
        return self.element_table.get_element_state(element_id)

    def set_state(self, element_id: str, state: ElementState):
        self.element_table.set_element_state(element_id, state)
        return self.get_state(element_id=element_id)

    # --------- SYSTEM STATE HANDLING SECTION --------- #

    def stop(self):
        self.set_model_state(ModelState.DIRT)
        self.element_table.update_state_by_type(ElementType.CLIENT, ElementState.STOP)
        self.element_table.update_state_by_type(ElementType.CLOUD, ElementState.STOP)

    def reset(self):
        self.set_model_state(ModelState.DIRT)
        self.element_table.update_state_by_type(ElementType.CLIENT, ElementState.RESET)
        self.element_table.update_state_by_type(ElementType.CLOUD, ElementState.RESET)

    # --------- CONFIGURATION HANDLING SECTION --------- #

    def get_servers_configuration(self):
        return Configuration(self.element_table.get_servers_configuration())

    def get_complete_configuration(self):
        configuration = self.element_table.get_complete_configuration()
        print(configuration)
        return Configuration(configuration)

