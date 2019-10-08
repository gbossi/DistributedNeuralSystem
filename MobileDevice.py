#Controller Client
#Connect to known server
#Put in wait state (5s) if everything not ready and ask again
#Get the settings
#Download the model
#Instantiate the model

#Log Client
#Connect to log server

#Cloud Client
#Connect to Cloud server


#Cycle get images from local file folder
#Predict
#Send the prediction to the cloud
#Check the state

import cv2
import numpy as np
from interfaces.ttypes import ElementType
from ClientComponents.ControllerClient import ControllerClient
from ClientComponents.LogClient import Logger

class MobileDevice:
    def __init__(self):
        self.controller = ControllerClient(ElementType.CLIENT).connect_to_configuration_server()
        self.remote_configurations = self.controller.register_and_get_configuration()
        self.keras_model = self.controller.download_model()
        self.logger = self.connect_to_log_server()
#       self.cloud_interface

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

#if __name__ == '__main__':

