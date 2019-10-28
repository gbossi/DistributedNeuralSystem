from .MasterController import MasterController
from interfaces.ttypes import ModelConfiguration, ModelState


class ExternalController(MasterController):

    def get_complete_configuration(self):
        """
        :return: all the element connected to the master server (id, type, ip, port)
        """
        return self.controller_interface.get_complete_configuration()

    def instantiate_model(self, model_name: str, split_layer: int):
        model_config = ModelConfiguration(model_name=model_name, split_layer=split_layer)
        self.controller_interface.set_model(model_config)

    def set_model_state(self, state: ModelState):
        return self.controller_interface.set_model_state(model_state=state)

    def stop(self):
        self.controller_interface.stop()

    def reset(self):
        self.controller_interface.reset()