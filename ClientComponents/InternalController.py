from .MasterController import MasterController
import time
import tensorflow as tf
from interfaces.ttypes import ElementState, ElementType

WAITING_TIME = 5


class InternalController(MasterController):
    def __init__(self, element_type: ElementType, server_ip='localhost', port=10100):
        super(InternalController, self).__init__(element_type, server_ip, port)

    def get_servers_configuration(self):
        """
        Wait until all the other server components are available, then it gets a server configuration
        from the master server
        :return: a list of server configuration (type, ip, port)
        """
        while self.current_state == ElementState.WAITING:
            time.sleep(WAITING_TIME)
            self.update_state()
        return self.controller_interface.get_servers_configuration()

    def update_state(self):
        self.current_state = self.controller_interface.get_state(self.element_id)
        return self.current_state

    def set_state(self, element_state: ElementState):
        self.current_state = self.controller_interface.set_state(self.element_id, element_state)

    def download_model(self):
        while not self.controller_interface.is_model_available:
            time.sleep(WAITING_TIME)

        batch_dimension = 100000  # 100 KB
        current_position = 0
        remaining = 1

        filename = {ElementType.CLIENT: "./client.h5",
                    ElementType.CLOUD: "./cloud.h5"
                    }[self.element_type]

        writer = open(filename, "wb")

        while remaining:
            file_chunk = self.controller_interface.get_model_chunk(self.element_type,
                                                                   current_position, batch_dimension)
            current_position += batch_dimension
            remaining = file_chunk.remaining
            if batch_dimension < remaining:
                batch_dimension = remaining
            writer.write(file_chunk.data)

        return tf.keras.models.load_model(filename)
