from ClientComponents.ExternalController import ExternalController
from ttypes import ElementType, ModelState
import time

IP_MASTER = "localhost"
MASTER_PORT = 10100
IMAGES_SOURCE = './images_source/'
BATCH_SIZE = 8

if __name__ == '__main__':
    controller = ExternalController(element_type=ElementType.CONTROLLER, server_ip=IP_MASTER, port=MASTER_PORT)
    controller.connect_to_configuration_server()
    controller.register_controller()
    controller.instantiate_model(model_name="VGG16", split_layer=8)
    controller.set_model_state(ModelState.AVAILABLE)
    time.sleep(120)
    controller.stop()


