from ClientComponents.ExternalController import ExternalController
from ttypes import ElementType, ModelState
import time

IP_MASTER = "localhost"
MASTER_PORT = 10100


if __name__ == '__main__':
    controller = ExternalController(element_type=ElementType.CONTROLLER, server_ip=IP_MASTER, port=MASTER_PORT)
    controller.connect_to_configuration_server()
    controller.register_controller()
    controller.instantiate_model(model_name="VGG16", split_layer=8)
    controller.set_model_state(ModelState.AVAILABLE)
    for i in range(50):
        time.sleep(5)
        print(controller.get_complete_configuration())
    controller.stop()


