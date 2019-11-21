from .MasterController import MasterController
from interfaces.ttypes import ModelConfiguration, ModelState, ElementType, Test, LogType


class ExternalController(MasterController):
    def __init__(self, server_ip='localhost', port=10100):
        super(ExternalController, self).__init__(server_ip, port)

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

    def is_test_over(self):
        return self.controller_interface.is_test_over()

    def stop(self):
        self.controller_interface.stop()

    def reset(self):
        self.controller_interface.reset()

    def download_log(self, log_type: LogType, saving_folder: str):
        batch_dimension = 100000  # 100 KB
        current_position = 0
        remaining = 1

        filename = {LogType.MESSAGE: "/message.csv",
                    LogType.PERFORMANCE: "/performance.csv",
                    LogType.SPECS: "/specs.csv"
                    }[log_type]

        filename = saving_folder + filename

        writer = open(filename, "wb")

        while remaining:
            file_chunk = self.logger_interface.get_log_chunk(log_type, current_position, batch_dimension)
            current_position += batch_dimension
            remaining = file_chunk.remaining
            if batch_dimension < remaining:
                batch_dimension = remaining
            writer.write(file_chunk.data)
