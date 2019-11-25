import tensorflow as tf


class ModelFactory:
    def get_new_model(self, model_name):
        if model_name == "VGG16":
            return tf.keras.applications.VGG16(weights='imagenet')
        elif model_name == "MobileNet":
            return tf.keras.applications.MobileNet(weights='imagenet')
        elif model_name == "VGG19":
            return tf.keras.applications.VGG19(weights='imagenet')
        elif model_name == "ResNet":
            return tf.keras.applications.ResNet50(weights='imagenet')
"""        elif model_name == "AlexNet":
            return tf.keras.applications.alexnetXXX
        elif model_name == "Yolo":
            return Yolo
"""
