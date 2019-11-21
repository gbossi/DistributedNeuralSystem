from ClientComponents.ExternalController import ExternalController
from ttypes import ElementType, ModelState, LogType
import time

IP_MASTER = "localhost"
MASTER_PORT = 10100


class Controller:
    def __init__(self):
        self.controller = ExternalController(element_type=ElementType.CONTROLLER, server_ip=IP_MASTER, port=MASTER_PORT)
        self.controller.register_controller()
        self.base_path = "./Computer/CNN"

    def perform_test(self,
                     model_name,
                     split_layer,
                     no_images,
                     edge_batch_size,
                     cloud_batch_size,
                     no_repetitions):
        self.setup_model(model_name=model_name, split_layer=split_layer)
        test_completed = 0
        while test_completed < no_repetitions:
            self.controller.set_test(True, number_of_images=no_images, edge_batch_size=edge_batch_size,
                                     cloud_batch_size=cloud_batch_size)
            while not self.controller.is_test_over():
                time.sleep(5)
                test_completed += 1
            path = self.base_path+"/"+model_name+"/split_layer_"+str(split_layer)+"/cloud_batch_"+ \
                   str(cloud_batch_size)+"/edge_batch_size_"+str(edge_batch_size)+"/no_images_"+ \
                   str(no_images)+"/"+time.strftime("%Y%m%d-%H:%M:%S", time.gmtime())+"/"+str(test_completed+1)+"/"
            self.download_all_logs(path)

    def download_all_logs(self, folder_path):
        self.controller.download_log(LogType.MESSAGE, folder_path)
        self.controller.download_log(LogType.PERFORMANCE, folder_path)

    def setup_model(self, model_name="VGG16", split_layer=8):
        self.controller.instantiate_model(model_name=model_name, split_layer=split_layer)
        self.controller.set_model_state(ModelState.AVAILABLE)

    def stop_system(self):
        self.controller.stop()


if __name__ == '__main__':
    controller = Controller()
    controller.perform_test("VGG19", split_layer=12, no_images=20, edge_batch_size=1, cloud_batch_size=1, no_repetitions=2)
    controller.stop_system()
