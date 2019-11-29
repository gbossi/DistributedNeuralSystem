from ClientComponents.ExternalController import ExternalController
from ttypes import ElementType, ModelState, LogType, ElementState
import time
import os

IP_MASTER = "localhost"
MASTER_PORT = 10100
WAITING_TIME = 5

class Controller:
    def __init__(self):
        self.controller = ExternalController(server_ip=IP_MASTER, port=MASTER_PORT)
        self.controller.register_element(ElementType.CONTROLLER)
        self.base_path = "./Computer/CNN"

    def start_system(self,
                     model_name,
                     split_layer,
                     edge_batch_size,
                     num_edges,
                     cloud_batch_size,
                     time_limit):
        self.setup_model(model_name=model_name, split_layer=split_layer)

        self.controller.set_test(False, number_of_images=0, edge_batch_size=0,
                                 cloud_batch_size=0)

        self.check_distributed_system(num_edges)

        time.sleep(time_limit)

        self.controller.stop()

    def perform_test(self,
                     model_name,
                     split_layer,
                     num_images,
                     num_edges,
                     edge_batch_size,
                     cloud_batch_size,
                     no_repetitions):
        self.setup_model(model_name=model_name, split_layer=split_layer)

        self.controller.set_test(True, number_of_images=num_images, edge_batch_size=edge_batch_size,
                                 cloud_batch_size=cloud_batch_size)
        test_completed = 0

        while test_completed < no_repetitions:
            self.check_distributed_system(num_edges)
            self.controller.run()

            while not self.controller.is_test_over():
                time.sleep(WAITING_TIME)

            test_completed += 1
            path = self.base_path+"/"+model_name+"/split_layer_"+str(split_layer)+"/cloud_batch_"+ \
                   str(cloud_batch_size)+"/edge_batch_size_"+str(edge_batch_size)+"/no_images_"+ \
                   str(num_images)+"/"+str(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))+"/"+str(
                test_completed)+"/"
            if not os.path.exists(path):
                os.makedirs(path)

            self.download_all_logs(path)

    def download_all_logs(self, folder_path):
        self.controller.download_log(LogType.MESSAGE, folder_path)
        self.controller.download_log(LogType.PERFORMANCE, folder_path)
        self.controller.download_log(LogType.SPECS, folder_path)

    def setup_model(self, model_name="VGG16", split_layer=8):
        self.controller.instantiate_model(model_name=model_name, split_layer=split_layer)
        self.controller.set_model_state(ModelState.AVAILABLE)

    def stop_system(self):
        self.controller.stop()

    def reset_system(self):
        self.controller.reset()

    def check_distributed_system(self, num_edges):
        current_edges = 0
        exist_cloud = False
        while current_edges < num_edges or not exist_cloud:
            current_config = self.controller.get_complete_configuration()
            clients = self.controller.get_element_type_from_configuration(current_config, ElementType.CLIENT)
            for client in clients:
                if client.state == ElementState.READY:
                    current_edges += 1
            clouds = self.controller.get_element_type_from_configuration(current_config, ElementType.CLOUD)
            for cloud in clouds:
                if cloud.state == ElementState.READY:
                    exist_cloud = True
            time.sleep(WAITING_TIME)


if __name__ == '__main__':
    controller = Controller()
    controller.perform_test("VGG19", split_layer=10, num_images=20, num_edges=1, edge_batch_size=1, cloud_batch_size=1,
                            no_repetitions=2)
    controller.reset_system()
    controller.perform_test("VGG19", split_layer=12, num_images=20, num_edges=1, edge_batch_size=1, cloud_batch_size=1,
                            no_repetitions=2)
    controller.stop_system()
