#Connect to known server
#Put in wait state (5s) if everything not ready and ask again
#Get the settings
#Connect to log server
#Connect to sink server
#Download the model
#Instantiate the model

import uuid, cv2
import numpy as np

class MobileDevice:
    def __init__(self):
        self.name = uuid.uuid4().hex


    @staticmethod
    def adapt_image_to_model_dimension(image_tuple, input_dimension):
        image_data = np.frombuffer(image_tuple.arr_bytes, dtype=image_tuple.data_type).reshape(
            image_tuple.shape)
        image_data = cv2.resize(image_data, tuple(input_dimension[0:2]), interpolation=cv2.INTER_AREA)
        return image_data

#if __name__ == '__main__':

