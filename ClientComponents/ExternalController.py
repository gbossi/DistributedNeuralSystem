from .MasterController import MasterController
from interfaces.ttypes import ModelConfiguration, ModelState, ElementType


class ExternalController(MasterController):
    def __init__(self, element_type: ElementType, server_ip='localhost', port=10100):
        super(ExternalController, self).__init__(element_type, server_ip, port)

    def get_complete_configuration(self):
        """
        :return: all the element connected to the master server (id, type, ip, port)
        """
        return self.controller_interface.get_complete_configuration()

    def instantiate_model(self, model_name: str, split_layer: int):
        self.controller_interface.instantiate_model(ModelConfiguration(model_name=model_name, split_layer=split_layer))

    def set_model_state(self, state: ModelState):
        return self.controller_interface.set_model_state(model_state=state)

    def stop(self):
        self.controller_interface.stop()

    def reset(self):
        self.controller_interface.reset()