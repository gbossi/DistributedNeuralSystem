import time
from thrift_interfaces.ttypes import ElementState, ElementType, PerformanceMessage
from src.components.client_components.master_controller import MasterController

WAITING_TIME = 5


class InternalController(MasterController):
    def __init__(self, server_ip='localhost', port=10100):
        super(InternalController, self).__init__(server_ip, port)
        self.last_update = 0
        self.model_id = None

    def wait_in_ready_state(self):
        while self.current_state == ElementState.READY:
            time.sleep(WAITING_TIME)
            self.update_state()

    def get_servers_configuration(self):
        """
        Wait until all the other server components are available, then it gets a server configuration
        from the master server
        :return: a list of server configuration (type, ip, port)
        """
        while not self.controller_interface.is_cloud_available():
            time.sleep(WAITING_TIME)
        return self.controller_interface.get_servers_configuration()

    def update_state(self):
        """
        Update the current element state every 5 seconds
        :return: current state
        """
        current_update = time.time()
        if current_update-self.last_update > 5:
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
        self.send_log('Getting a new test')
        self.set_state(ElementState.READY)
        self.wait_in_ready_state()
        return self.controller_interface.get_test(self.element_type)

    def test_completed(self):
        self.send_log('Completed test')
        self.controller_interface.test_completed()

    def download_model(self):
        self.send_log('Waiting for a new model')
        self.model_id = self.controller_interface.get_model_id(self.element_id)
        model_set = self.controller_interface.is_model_available(self.element_id, self.model_id)
        while not model_set:
            self.model_id = self.controller_interface.get_model_id(self.element_id)
            model_set = self.controller_interface.is_model_available(self.element_id, self.model_id)
            time.sleep(WAITING_TIME)

        self.send_log('Downloading a new model')
        batch_dimension = 1000000  # 1 MB
        current_position = 0
        remaining = 1

        filename = {ElementType.CLIENT: "./client.h5",
                    ElementType.CLOUD: "./cloud.h5"
                    }[self.element_type]

        writer = open(filename, "wb")

        while remaining:
            file_chunk = self.controller_interface.get_model_chunk(self.element_id,
                                                                   current_position, batch_dimension)
            current_position += batch_dimension
            remaining = file_chunk.remaining
            if batch_dimension < remaining:
                batch_dimension = remaining
            writer.write(file_chunk.data)

        return filename

    def log_performance_message(self, no_images_predicted: int, images_ids: str, elapsed_time: float):
        self.__log_performance__(no_images_predicted=no_images_predicted,
                                 images_ids=images_ids,
                                 elapsed_time=elapsed_time)

    def log_performance_message_and_shape(self, no_images_predicted: int, images_ids: str, elapsed_time: float, shape):
        self.__log_performance__(no_images_predicted=no_images_predicted,
                                 images_ids=images_ids,
                                 elapsed_time=elapsed_time,
                                 output_dimension=shape)

    def log_performance_message_and_result(self, no_images_predicted: int, images_ids: str, elapsed_time: float,
                                           predicted: str):
        self.__log_performance__(no_images_predicted=no_images_predicted,
                                 images_ids=images_ids,
                                 elapsed_time=elapsed_time,
                                 predicted=predicted)

    def __log_performance__(self, no_images_predicted: int,
                            images_ids: str,
                            elapsed_time: float,
                            predicted=None,
                            output_dimension=None):

        if output_dimension is None:
            output_dimension = [1, 1]
        if predicted is None:
            predicted = "Nan"

        self.logger_interface.log_performance_message(
            PerformanceMessage(timestamp=time.time(),
                               id=self.element_id,
                               element_type=self.element_type,
                               no_images_predicted=no_images_predicted,
                               list_ids=str(images_ids),
                               elapsed_time=elapsed_time,
                               decoded_ids=predicted,
                               output_dimension=output_dimension))
