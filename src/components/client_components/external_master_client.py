from src.components.client_components.master_client import MasterClient
from thrift_interfaces.ttypes import ModelConfiguration, Test, LogType


class ExternalClient(MasterClient):
    def __init__(self, server_ip, port):
        super(ExternalClient, self).__init__(server_ip, port)

    def get_complete_configuration(self):
        """
        :return: all the element connected to the master server (id, type, ip, port)
        """
        return self.controller_interface.get_complete_configuration()

    def instantiate_model(self, model_name: str, split_layer: int):
        self.send_log('Controller Model Setup')
        gen_model_id = self.controller_interface.instantiate_model(ModelConfiguration(model_name=model_name,
                                                                                      split_layer=split_layer))
        return gen_model_id


    def set_test(self, is_test: bool, number_of_images: int, edge_batch_size: int, cloud_batch_size: int):
        self.send_log('Setting a new test')
        self.test_id = self.controller_interface.set_test(Test(is_test=is_test,
                                                               number_of_images=number_of_images,
                                                               edge_batch_size=edge_batch_size,
                                                               cloud_batch_size=cloud_batch_size))

    def download_log(self, log_type: LogType, saving_folder: str):
        self.send_log('Downloading all the logs')
        self.logger_interface.prepare_log(log_type=log_type)

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

        return filename

    def assign_model(self, element_id, model_id):
        self.controller_interface.zip_model_element(element_id, model_id)

    def reset_model(self, element_id):
        self.controller_interface.zip_model_element(element_id, 'NO_MODEL')

    def assign_test(self, element_id):
        self.controller_interface.zip_test_element(element_id, self.test_id)

    def reset_test(self, element_id):
        self.controller_interface.zip_test_element(element_id, 'NO_TEST')

    def assign_state(self, element_id, element_state):
        self.controller_interface.set_state(element_id, element_state)
