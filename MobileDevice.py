#Controller Client
#Connect to known server V
#Put in wait state (5s) if everything not ready and ask again V
#Get the settings V
#Download the model V
#Instantiate the model V

#Log Client
#Connect to log server V

#Cloud Client
#Connect to Cloud server


#Cycle get images from local file folder
#Predict
#Send the prediction to the cloud
#Check the state

import cv2
import numpy as np
from interfaces.ttypes import ElementType, ElementState
from ClientComponents.ControllerClient import ControllerClient
from ClientComponents.LogClient import Logger

class MobileDevice:
    def __init__(self):
        self.element_type = ElementType.CLIENT
        self.controller = ControllerClient(self.element_type)
        self.controller.connect_to_configuration_server()
        self.controller.register_controller()
        self.controller.set_state(ElementState.RUNNING)
        self.remote_configurations = self.controller.get_servers_configuration()
        #self.keras_model = self.controller.download_model()
        #self.cloud_interface = self.connect_to_cloud()

    def send_log(self, message):
        self.controller.send_log(message)

    def get_server_from_configuration(self, type: ElementType):
        for server_config in self.remote_configurations:
            if type == server_config.type:
                return server_config

    def connect_to_log_server(self):
        log_config = self.get_server_from_configuration(ElementType.LOGGER)
        return Logger(conf_server_ip=log_config.ip, port=log_config.port).connect_to_logger_server()


#    def connect_to_cloud_server(self):


    @staticmethod
    def adapt_image_to_model_dimension(image_tuple, input_dimension):
        image_data = np.frombuffer(image_tuple.arr_bytes, dtype=image_tuple.data_type).reshape(
            image_tuple.shape)
        image_data = cv2.resize(image_data, tuple(input_dimension[0:2]), interpolation=cv2.INTER_AREA)
        return image_data

if __name__ == '__main__':
    client = MobileDevice()
    client.send_log("ciao")


