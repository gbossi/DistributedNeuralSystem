from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, UpSampling2D
from tensorflow.keras.models import Model

def Encoder():
    input_img = Input(shape=(28, 28, 1))  # adapt this if using `channels_first` image data format
    conv1 = Conv2D(32, (3, 3), activation='relu', padding='same')(input_img)  # 28 x 28 x 32
    pool1 = MaxPooling2D(pool_size=(2, 2))(conv1)  # 14 x 14 x 32
    conv2 = Conv2D(64, (3, 3), activation='relu', padding='same')(pool1)  # 14 x 14 x 64
    pool2 = MaxPooling2D(pool_size=(2, 2))(conv2)  # 7 x 7 x 64
    conv3 = Conv2D(128, (3, 3), activation='relu', padding='same')(pool2)  # 7 x 7 x 128
    return Model(input_img, conv3)


def Decoder():
    input_img = Input(shape=(4, 4, 8))  # adapt this if using `channels_first` image data format
    # decoder
    conv4 = Conv2D(128, (3, 3), activation='relu', padding='same')(conv3)  # 7 x 7 x 128
    up1 = UpSampling2D((2, 2))(conv4)  # 14 x 14 x 128
    conv5 = Conv2D(64, (3, 3), activation='relu', padding='same')(up1)  # 14 x 14 x 64
    up2 = UpSampling2D((2, 2))(conv5)  # 28 x 28 x 64
    decoded = Conv2D(1, (3, 3), activation='sigmoid', padding='same')(up2)  # 28 x 28 x 1
    return Model(input_img, decoded)

x = Input something....
autoencoder = Model(x, Decoder()(Encoder()(x)))
autoencoder.compile(optimizer='adadelta')