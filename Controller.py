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
    controller.set_test(True, number_of_images=100, edge_batch_size=1, cloud_batch_size=2)
    for i in range(50):
        time.sleep(5)
        print(controller.get_complete_configuration())
    controller.stop()


