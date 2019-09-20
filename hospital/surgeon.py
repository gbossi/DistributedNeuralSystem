import tensorflow as tf
import uuid


class Surgeon:

    def split(self, model, split_layer: int):
        """ Given a model or a location in the filesystem
         and a point inside the network where to split
        the neural network, return two neural networks"""

        model = self.check_model(model)
        assert isinstance(model, tf.keras.Model)
        input_shape = model.layers[split_layer].input_shape[1:]
        m_input = tf.keras.Input(input_shape)
        model_layers = m_input
        for layer in model.layers[split_layer:]:
            model_layers = layer(model_layers)

        # Give a unique name that contains the information of the models
        modelA = tf.keras.Model(inputs=model.input, outputs=model.layers[split_layer-1].output,
                                trainable=False, name=model.name+"_0-"+str(split_layer)+"_"+str(uuid.uuid1()))
        modelB = tf.keras.Model(inputs=m_input, outputs=model_layers,
                                trainable=False, name=model.name+"_"+str(split_layer)+"-"+
                                                      str(len(model.layers))+"_"+str(uuid.uuid1()))
        return modelA, modelB

    def merge(self, modelA, modelB, merge_layer: int, is_trainable=False):
        """ Given two previously concatenated model
        it reconcatenates the model and return a
        unique model equal to the original one"""

        modelA = self.check_model(modelA)
        modelB = self.check_model(modelB)

        self.check_compatibility(modelA, modelB)
        input_shape = modelA.layers[1].input_shape[1:]
        m_input = tf.keras.Input(input_shape)
        model_layers = m_input

        for layer in modelA.layers[:merge_layer]+modelB.layers[1:]:
            model_layers = layer(model_layers)

        model = tf.keras.Model(inputs=m_input, outputs=model_layers, trainable=is_trainable)
        return model

    def split_and_add_autoencoder(self, model, autoencoder, encoder_layer: int):
        """ Given a model and an autoencoder trained on a particular layer of
        the neural network it returns two model with the encoder at the end of the
        first model and the decoder at the beginning of the second model"""
        model = self.check_model(model)
        modelA, modelB = self.split(model, encoder_layer)
        return self.add_autoencoder(modelA, modelB, autoencoder)

    def add_autoencoder(self, modelA, modelB, autoencoder):
        modelA = self.check_model(modelA)
        modelB = self.check_model(modelB)
        autoencoder = self.check_model(autoencoder)
        n_layer_autoencoder = len(autoencoder.layers)
        encoder, decoder = self.split(autoencoder, int(n_layer_autoencoder / 2))
        return self.add_autoencoder(modelA, modelB, encoder, decoder)

    def add_autoencoder(self, modelA, modelB, decoder, encoder):
        modelA = self.merge(modelA, encoder)
        modelB = self.merge(decoder, modelB)
        return modelA, modelB

    def check_compatibility(self, modelA: tf.keras.Model, modelB):
        if modelA.layers[-1].output_shape == modelB.layers[1].input_shape:
            return True
        else:
            raise Exception("Not compatible input and output of the merging models")

    def check_model(self, model):
        """ This method check that the filepath or
        the model itself are instances of a Keras model """
        if isinstance(model, str):
            model = tf.keras.model.load_model(model)
        if not isinstance(model, tf.keras.Model):
            raise Exception("Not keras compatible model")
        return model




