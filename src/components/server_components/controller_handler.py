import os
import uuid
import shutil
import pandas as pd
import tensorflow as tf
from src.utils.model_factory import ModelFactory
from src.utils.surgeon import Surgeon
from pathlib import Path
from thrift_interfaces.ttypes import Configuration, ElementConfiguration, ElementType, ElementState, FileChunk, Test
from thrift_interfaces.ttypes import ModelConfiguration


class ControllerInterfaceService:
    def __init__(self):
        self.surgeon = Surgeon()
        self.device_model_path_dict = {}
        self.server_model_path_dict = {}
        self.model_factory = ModelFactory()
        self.element_table = ElementTable()
        self.test_table = TestTable()

    # --------- MODEL HANDLING SECTION --------- #

    def instantiate_model(self, model_configuration: ModelConfiguration):
        """
        Given a configuration, this function initializes the model that
        the servers and the client will download

        :param model_configuration: A model name and a split layer
        :return: None
        """
        model = self.model_factory.get_new_model(model_configuration.model_name)
        device_model, server_model, model_id = self.surgeon.split(model, model_configuration.split_layer)

        device_base_path = "./models/client/"
        server_base_path = "./models/server/"

        if not os.path.exists(device_base_path):
            os.makedirs(device_base_path)
        else:
            shutil.rmtree(device_base_path)
            os.makedirs(device_base_path)
        if not os.path.exists(server_base_path):
            os.makedirs(server_base_path)
        else:
            shutil.rmtree(server_base_path)
            os.makedirs(server_base_path)

        device_model_path = device_base_path+device_model.name
        self.device_model_path_dict.update({model_id: device_model_path})
        Path(device_model_path+".h5").touch()
        device_model.save(device_model_path+".h5")

        device_arm_model = self.surgeon.convert_model(device_model)
        open(device_model_path + ".tflite", "wb").write(device_arm_model)

        server_model_path = server_base_path+server_model.name
        self.server_model_path_dict.update({model_id: server_model_path})
        Path(server_model_path+".h5").touch()
        server_model.save(server_model_path+".h5")
        tf.keras.backend.clear_session()

        return model_id

    def get_model_id(self, element_id):
        model_id = self.element_table.get_model_id(element_id)
        if model_id == 'NO_MODEL' or model_id is None:
            return 'MODEL NOT AVAILABLE'
        else:
            return model_id

    def zip_model_element(self, element_id, model_id):
        self.element_table.update_model(element_id, model_id)

    def is_model_available(self, element_id, model_id):
        if model_id == self.element_table.get_model_id(element_id):
            return True
        else:
            return False

    def get_model_chunk(self, element_id, offset: int, size: int):
        """
        Function used to download the partial neural network model by the
        clients and the computational server, depending on the type it will
        return a different model

        :param server_type: define the type of the model to be sent
        :param offset: define the offset
        :param size: define the size requested
        :return: a binary file chunk
        """

        type = self.element_table.get_element_type(element_id)
        tensorflow_type = self.element_table.get_element_tensorflow_type(element_id)
        reader = None
        model_id = self.element_table.get_model_id(element_id)
        device_model_path = self.device_model_path_dict.get(model_id)
        server_model_path = self.server_model_path_dict.get(model_id)

        if type == ElementType.CLIENT:
            if tensorflow_type == 'tensorflow':
                reader = open(device_model_path+".h5", "rb")
            else:
                reader = open(device_model_path+".tflite", "rb")
        if type == ElementType.CLOUD:
            reader = open(server_model_path+".h5", "rb")

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
            self.element_table.insert(element_id,
                                      local_config.type,
                                      local_config.architecture,
                                      local_config.tensorflow_type,
                                      local_config.ip,
                                      local_config.port)
        elif local_config.type is ElementType.CLIENT:
            self.element_table.insert(element_id,
                                      local_config.type,
                                      local_config.architecture,
                                      local_config.tensorflow_type)
        elif local_config.type is ElementType.CONTROLLER:
            self.element_table.insert(element_id,
                                      local_config.type,
                                      local_config.architecture,
                                      local_config.tensorflow_type,
                                      element_state=ElementState.RUNNING)

        return element_id

    def get_state(self, element_id):
        return self.element_table.get_element_state(element_id)

    def is_cloud_available(self):
        return self.element_table.exist_type(ElementType.CLOUD)

    def set_state(self, element_id: str, state: ElementState):
        self.element_table.set_element_state(element_id, state)
        return self.get_state(element_id=element_id)

    # --------- CONFIGURATION HANDLING SECTION --------- #

    def get_servers_configuration(self):
        return Configuration(self.element_table.get_servers_configuration())

    def get_complete_configuration(self):
        return Configuration(self.element_table.get_complete_configuration())

    # --------- TEST CONFIGURATION SECTION ------------- #

    def set_test(self, test: Test):
        return self.test_table.insert(test)

    def zip_test_element(self, element_id, test_id):
        self.element_table.update_test(element_id, test_id)

    def get_test_id(self, element_id):
        return self.element_table.get_test_id(element_id)

    def get_test(self, test_id: str):
        return self.test_table.get_test_specs(test_id)

    def test_completed(self, test_id: str):
        self.test_table.add_waiting(test_id)

    def is_test_over(self, test_id: str):
        return self.test_table.end_status(test_id)


class TestTable:
    def __init__(self):
        self.test_table = pd.DataFrame()

    def insert(self, test: Test):
        test_id = str(uuid.uuid4().hex)
        new_row = pd.DataFrame([{'number_of_images': test.number_of_images,
                                 'cloud_batch_size': test.cloud_batch_size,
                                 'edge_batch_size': test.edge_batch_size,
                                 'test_started': False,
                                 'elements_running': 0,
                                 'elements_waiting': 0,
                                 'test_completed': 0,
                                 'test_procedure': test.is_test}], index=[test_id])
        self.test_table = self.test_table.append(new_row)
        return test_id

    def get_test_specs(self, test_id):
        self.test_table.at[test_id, 'elements_running'] = self.test_table.at[test_id, 'elements_running'] + 1
        return Test(is_test=self.test_table.at[test_id, 'test_procedure'],
                    number_of_images=self.test_table.at[test_id, 'number_of_images'],
                    cloud_batch_size=self.test_table.at[test_id, 'cloud_batch_size'],
                    edge_batch_size=self.test_table.at[test_id, 'edge_batch_size'])

    def add_waiting(self, test_id):
        self.test_table.at[test_id, 'test_started'] = True
        self.test_table.at[test_id, 'elements_waiting'] = self.test_table.at[test_id, 'elements_waiting'] + 1

    def end_status(self, test_id):
        started = self.test_table.at[test_id, 'test_started']
        elements_running = self.test_table.at[test_id, 'elements_running']
        test_completed = self.test_table.at[test_id, 'test_completed']
        elements_waiting = self.test_table.at[test_id, 'elements_waiting']
        if started and elements_running * (test_completed+1) == elements_waiting:
            self.test_table.at[test_id, 'test_completed'] = self.test_table.at[test_id, 'test_completed']+1
            return True
        else:
            return False


class ElementTable:
    def __init__(self):
        self.elements_table = pd.DataFrame()

    def insert(self, element_id, element_type, architecture, tensorflow_type,  element_ip='unavailable', element_port=0,
               element_state=ElementState.WAITING):
        new_row = pd.DataFrame([{'type': element_type,
                                 'ip': element_ip,
                                 'architecture': architecture,
                                 'tensorflow_type': tensorflow_type,
                                 'port': element_port,
                                 'state': element_state,
                                 'model_id': None,
                                 'test_id': None}], index=[element_id])
        self.elements_table = self.elements_table.append(new_row)

    def get_servers_configuration(self):
        filter_configuration = self.elements_table[self.elements_table['type'] != ElementType.CLIENT]
        elements_configurations = []
        for element in filter_configuration.itertuples(index=False):
            elements_configurations += [ElementConfiguration(type=getattr(element, 'type'),
                                                             ip=getattr(element, 'ip'),
                                                             port=getattr(element, 'port'))]
        return elements_configurations

    def get_complete_configuration(self):
        elements_configurations = []
        for element in self.elements_table.itertuples():
            elements_configurations += [ElementConfiguration(id=element.Index,
                                                             type=getattr(element, 'type'),
                                                             ip=getattr(element, 'ip'),
                                                             port=getattr(element, 'port'),
                                                             state=getattr(element, 'state'),
                                                             architecture=getattr(element, 'architecture'),
                                                             tensorflow_type=getattr(element, 'tensorflow_type'),
                                                             model_id=getattr(element, 'model_id'),
                                                             test_id=getattr(element, 'test_id'))]
        return elements_configurations

    def get_element_state(self, element_id):
        return self.elements_table.at[element_id, 'state']

    def get_element_type(self, element_id):
        return self.elements_table.at[element_id, 'type']

    def get_element_tensorflow_type(self, element_id):
        return self.elements_table.at[element_id, 'tensorflow_type']

    def get_model_id(self, element_id):
        return self.elements_table.at[element_id, 'model_id']

    def set_element_state(self, element_id, state):
        self.elements_table.at[element_id, 'state'] = state
        return self.get_element_state(element_id)

    def exist_type_in_state(self, element_type: ElementType, element_state: ElementState):
        if element_state in self.elements_table[self.elements_table['type'] == element_type].values:
            return True
        else:
            return False

    def exist_type(self, element_type: ElementType):
        return (self.elements_table['type'] == element_type).any()

    def update_state_by_type(self, element_type: ElementType, state: ElementState):
        self.elements_table.loc[self.elements_table['type'] == element_type, 'state'] = state

    def update_model(self, element_id, model_id):
        self.elements_table.at[element_id, 'model_id'] = model_id

    def update_test(self, element_id, test_id):
        self.elements_table.at[element_id, 'test_id'] = test_id

    def get_test_id(self, element_id):
        return self.elements_table.at[element_id, 'test_id']
