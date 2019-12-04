import os
import uuid
import sys
import shutil
from src.utils.element_table import ElementTable
from src.utils.model_factory import ModelFactory
from src.utils.surgeon import Surgeon
from pathlib import Path

sys.path.append("gen-py")
from interfaces.ttypes import Configuration, ElementConfiguration, ElementType, ElementState, FileChunk, Test
from interfaces.ttypes import ModelState, ModelConfiguration


class ControllerInterfaceService:
    def __init__(self):
        self.device_model_path = None
        self.server_model_path = None
        self.model_state = ModelState.UNSET
        self.element_table = ElementTable()
        self.test_settings = None

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

        device_base_path = "./models/client/"
        server_base_path = "./models/server/"

        if not os.path.exists(device_base_path):
            os.makedirs(device_base_path)
        else:
            shutil.rmtree(device_base_path)
        if not os.path.exists(server_base_path):
            os.makedirs(server_base_path)
        else:
            shutil.rmtree(server_base_path)

        self.device_model_path = device_base_path+device_model.name+".h5"
        Path(self.device_model_path).touch()
        device_model.save(self.device_model_path)

        self.server_model_path = server_base_path+server_model.name+".h5"
        Path(self.server_model_path).touch()
        server_model.save(self.server_model_path)

        return model_configuration

    def set_model_state(self, model_state: ModelState):
        if model_state is ModelState.DIRT:
            # todo delete old model
            pass
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

    def get_state(self, element_id):
        return self.element_table.get_element_state(element_id)

    def is_cloud_available(self):
        return self.element_table.exist_type(ElementType.CLOUD)

    def set_state(self, element_id: str, state: ElementState):
        self.element_table.set_element_state(element_id, state)
        return self.get_state(element_id=element_id)

    # --------- SYSTEM STATE HANDLING SECTION --------- #

    def run(self):
        self.element_table.update_state_by_type(ElementType.CLIENT, ElementState.RUNNING)
        self.element_table.update_state_by_type(ElementType.CLOUD, ElementState.RUNNING)

    def wait(self):
        self.element_table.update_state_by_type(ElementType.CLIENT, ElementState.WAITING)
        self.element_table.update_state_by_type(ElementType.CLOUD, ElementState.WAITING)

    def stop(self):
        self.element_table.update_state_by_type(ElementType.CLIENT, ElementState.STOP)
        self.element_table.update_state_by_type(ElementType.CLOUD, ElementState.STOP)

    def reset(self):
        self.model_state = ModelState.DIRT
        self.test_settings = None
        self.element_table.update_state_by_type(ElementType.CLIENT, ElementState.RESET)
        self.element_table.update_state_by_type(ElementType.CLOUD, ElementState.RESET)

    # --------- CONFIGURATION HANDLING SECTION --------- #

    def get_servers_configuration(self):
        return Configuration(self.element_table.get_servers_configuration())

    def get_complete_configuration(self):
        return Configuration(self.element_table.get_complete_configuration())

    # --------- TEST CONFIGURATION SECTION ------------- #

    def set_test(self, settings):
        if self.test_settings is not None:
            self.reset()
        self.test_settings = TestSettings(test=settings)

    def get_test(self, element_type: ElementType):
        if element_type in [ElementType.CLIENT, ElementType.CLOUD]:
            self.test_settings.add_running()
        return self.test_settings.get_test_specs()

    def test_completed(self):
        self.test_settings.add_waiting()

    def is_test_over(self):
        return self.test_settings.end_status()


class TestSettings:
    def __init__(self, test: Test):
        self.values = test
        self.started = False
        self.elements_running = 0
        self.elements_waiting = 0

    def get_test_specs(self):
        return self.values

    def add_running(self):
        self.elements_running += 1
        self.started = True

    def add_waiting(self):
        self.elements_waiting += 1

    def end_status(self):
        if self.started and self.elements_running == self.elements_waiting:
            self.elements_running = self.elements_running * 2
            return True
        else:
            return False

    def reset_test(self):
        self.started = False
        self.elements_running = 0
        self.elements_waiting = 0
