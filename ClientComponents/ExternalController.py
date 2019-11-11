from .MasterController import MasterController
from interfaces.ttypes import ModelConfiguration, ModelState, ElementType, Test


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

    def set_test(self, is_test: bool, number_of_images: int, edge_batch_size: int, cloud_batch_size: int):
        self.controller_interface.set_test(Test(is_test=is_test, number_of_images=number_of_images,
                                                edge_batch_size=edge_batch_size, cloud_batch_size=cloud_batch_size))

    def stop(self):
        self.controller_interface.stop()

    def reset(self):
        self.controller_interface.reset()