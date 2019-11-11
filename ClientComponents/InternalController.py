from .MasterController import MasterController
import time
import tensorflow as tf
from interfaces.ttypes import ElementState, ElementType, PerformanceMessage

WAITING_TIME = 5


class InternalController(MasterController):
    def __init__(self, element_type: ElementType, server_ip='localhost', port=10100):
        super(InternalController, self).__init__(element_type, server_ip, port)
        self.last_update = 0

    def get_servers_configuration(self):
        """
        Wait until all the other server components are available, then it gets a server configuration
        from the master server
        :return: a list of server configuration (type, ip, port)
        """
        while self.current_state == ElementState.WAITING:
            self.update_state()
        return self.controller_interface.get_servers_configuration()

    def update_state(self):
        """
        Update the current element state every 5 seconds
        :return: current state
        """
        current_update = time.time()
        if current_update-self.last_update > 5:
            print("updating state")
            self.last_update = current_update
            self.current_state = self.controller_interface.get_state(self.element_id)
        return self.current_state

    def set_state(self, element_state: ElementState):
        """
        Update the state of the element and force a local update of the value
        :param element_state:
        :return:
        """
        self.current_state = self.controller_interface.set_state(self.element_id, element_state)

    def get_test(self):
        return self.controller_interface.get_test()

    def download_model(self):
        while not self.controller_interface.is_model_available():
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

    def log_performance_message(self, no_images_predicted: int, images_ids: str, elapsed_time: float):
        self.logger_interface.log_performance_message(
            PerformanceMessage(time.time(),
                               self.element_id,
                               self.element_type,
                               no_images_predicted,
                               str(images_ids),
                               elapsed_time))
