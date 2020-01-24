import tensorflow as tf


class ModelFactory:
    def get_new_model(self, model_name):
        filename=None
        if model_name == "VGG16":
            filename = './.keras/models/vgg16.h5'
        elif model_name == "MobileNet":
            filename = './.keras/models/mobilenet.h5'
        elif model_name == "VGG19":
            filename = './.keras/models/vgg19.h5'
        elif model_name == "ResNet50":
            filename = './.keras/models/resnet50.h5'
        elif model_name == "Yolo":
            filename = './.keras/models/yolo_v3.h5'
        elif model_name == "AlexNet":
            filename = './.keras/models/alexnet_weights.h5'
        if filename is not None:
            return tf.keras.models.load_model(filename)
        else:
            raise Exception("File not Found")

