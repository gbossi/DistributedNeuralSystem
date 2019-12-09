import tensorflow as tf


class ModelFactory:
    def get_new_model(self, model_name):
        filename=None
        if model_name == "VGG16":
            filename = './.keras/models/vgg16_weights_tf_dim_ordering_tf_kernels.h5'
        elif model_name == "MobileNet":
            filename = './.keras/models/mobilenet_1_0_224_tf.h5'
        elif model_name == "VGG19":
            filename = './.keras/models/vgg19_weights_tf_dim_ordering_tf_kernels.h5'
        elif model_name == "ResNet":
            filename = './.keras/models/resnet50_weights_tf_dim_ordering_tf_kernels.h5'
        elif model_name == "Yolo":
            filename = './.keras/models/yolo_v3.h5'
        elif model_name == "AlexNet":
            filename = './.keras/models/alexnet_weights.h5'
        if filename is not None:
            return tf.keras.models.load_model(filename)
        else:
            raise Exception("File not Found")

"""        elif model_name == "AlexNet":
            return tf.keras.applications.alexnetXXX

"""
