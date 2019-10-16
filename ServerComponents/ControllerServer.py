from utils.model_factory import ModelFactory
from utils.surgeon import Surgeon
from interfaces.ttypes import Configuration, ElementConfiguration, ElementType, ElementState, FileChunk
from interfaces.ttypes import ModelState, ModelConfiguration
import os, uuid
import pandas as pd

# todo the following class need to stay inside utils external class
class ElementTable:
    def __init__(self):
        self.elements_table = pd.DataFrame()

    def insert(self, element_id, element_type, element_ip='unavailable', element_port=0,
               element_state=ElementState.WAITING):
        new_row = pd.DataFrame([{'type': element_type, 'ip': element_ip,
                                 'port': element_port, 'state': element_state}], index=[element_id])
        self.elements_table = self.elements_table.append(new_row)

    def trigger_state(self):
        if self.exist_waiting_type(ElementType.SINK):
            self.update_state_by_type(ElementType.SINK, ElementState.RUNNING)
            if self.exist_waiting_type(ElementType.CLOUD):
                self.update_state_by_type(ElementType.CLOUD, ElementState.RUNNING)
                if self.exist_waiting_type(ElementType.CLIENT):
                    self.update_state_by_type(ElementType.CLIENT, ElementState.RUNNING)

    def get_server_configuration(self):
        filter_configuration = self.elements_table[self.elements_table['type'] != ElementType.CLIENT]
        elements_configurations = []
        for element in filter_configuration.itertuples(index=False):
            elements_configurations += [ElementConfiguration(getattr(element, 'type'), getattr(element, 'ip'),
                                                             getattr(element, 'port'))]
        return elements_configurations

    def get_element_state(self, element_id):
        return self.elements_table.loc[[element_id], ['state']].values[0].item()

    def set_element_state(self, element_id, state):
        self.elements_table.at[element_id, 'state'] = state
        return self.get_element_state(element_id)

    def exist_waiting_type(self, element_type: ElementType):
        if ElementState.WAITING in self.elements_table['type' == element_type]:
            return True
        else:
            return False

    def update_state_by_type(self, element_type: ElementType, state: ElementState):
        self.elements_table.loc[self.elements_table['type'] == element_type, 'state'] = state


class ControllerInterfaceService:
    # The following init should be made by the master server !!!! #TODO
    def __init__(self):
        self.device_model_path = "./models/client/"
        self.server_model_path = "./models/server/"
        self.model_state = ModelState.UNSET
        self.element_table = ElementTable()

        # TODO The following line should be made by external controller
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

    def set_state(self, element_id: str, state: ElementState):
        self.element_table.set_element_state(element_id, state)
        return self.get_state(element_id=element_id)

    def register_element(self, local_config: ElementConfiguration):
        element_id = str(uuid.uuid4().hex)
        if local_config.type in [ElementType.CONTROLLER, ElementType.LOGGER, ElementType.CLOUD]:
            self.element_table.insert(element_id, local_config.type, local_config.ip, local_config.port)
        elif local_config.type is ElementType.CLIENT:
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
                  ElementType.CLOUD: open(self.server_model_path, "rb")
                  }[server_type]

        reader.seek(offset)
        data = reader.read(size)
        current_position = reader.tell()
        reader.seek(0, 2)

        return FileChunk(data, remaining=reader.tell()-current_position)
