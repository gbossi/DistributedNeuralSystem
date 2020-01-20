import time
import os
import csv
import pandas as pd
from src.components.client_components.external_controller import ExternalController
from thrift_interfaces.ttypes import ElementType, ModelState, LogType, ElementState

WAITING_TIME = 5


class Controller:
    def __init__(self, master_ip, master_port):
        self.controller = ExternalController(server_ip=master_ip, port=master_port)
        self.controller.register_element(ElementType.CONTROLLER)
        self.base_path = "./Computer/CNN"
        self.last_model_id = None

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

        self.controller.set_system_stop_state()

    def perform_test(self,
                     model_name,
                     split_layer,
                     num_images,
                     num_edges,
                     edge_batch_size,
                     cloud_batch_size,
                     no_repetitions):
        model_id = self.setup_model(model_name=model_name, split_layer=split_layer)

        self.controller.set_test(True, number_of_images=num_images, edge_batch_size=edge_batch_size,
                                 cloud_batch_size=cloud_batch_size)
        test_completed = 0

        while test_completed < no_repetitions:
            self.check_distributed_system(num_edges, model_id)
            self.controller.set_system_run_state()

            while not self.controller.is_test_over():
                time.sleep(WAITING_TIME)
                print(self.controller.get_complete_configuration())

            test_completed += 1
            path = self.base_path+'/'+model_name+'/split_layer_'+str(split_layer)+'/cloud_batch_' + \
                   str(cloud_batch_size)+'/edge_batch_size_'+str(edge_batch_size)+'/no_images_' + \
                   str(num_images)+'/'+str(time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime()))+'/' + \
                   str(test_completed)+'/'
            if not os.path.exists(path):
                os.makedirs(path)

            self.controller.download_log(LogType.MESSAGE, path)
            filename = self.controller.download_log(LogType.PERFORMANCE, path)
            self.complete_performance_csv(filename, model_name, split_layer, encoding=False)
            self.controller.download_log(LogType.SPECS, path)
            self.controller.send_log('Test #' + str(test_completed) + ' completed')

    @staticmethod
    def complete_performance_csv(filename, model_name, split_layer, encoding):
        df = pd.read_csv(filename)
        df["model_name"] = model_name
        df["split_layer"] = split_layer
        df["encoding"] = encoding
        df.to_csv(filename,  index=False)

    def setup_model(self, model_name, split_layer):
        model_id = self.controller.instantiate_model(model_name=model_name, split_layer=split_layer)
        self.controller.set_model_state(ModelState.AVAILABLE)
        return model_id

    def stop_system(self):
        self.controller.set_system_stop_state()

    def reset_system(self):
        self.controller.set_system_reset_state()

    def check_distributed_system(self, num_edges, model_id):
        '''
        Wait until there are a number of edge element connected greater of equal to the one requested, then assign a
        model to the specified number of edges and finally it wait until all the edges download the model from the
        master server and change the state into a ready
        
        :param num_edges: number of desired edges connected to the system
        :param model_id: model id
        :return:
        '''

        if self.last_model_id != model_id:
            self.last_model_id = model_id
            self.check_system_elements_in_state(num_edges, ElementState.WAITING)

            current_config = self.controller.get_complete_configuration()
            print(current_config)
            clients = self.controller.get_element_type_from_configuration(current_config, ElementType.CLIENT)
            for i in range(num_edges):
                if clients[i].state == ElementState.WAITING:
                    self.controller.assign_model(clients[i].id, model_id)
            clouds = self.controller.get_element_type_from_configuration(current_config, ElementType.CLOUD)
            for cloud in clouds:
                if cloud.state == ElementState.WAITING:
                    self.controller.assign_model(cloud.id, model_id)

        self.check_system_elements_in_state(num_edges, ElementState.READY)
        return

    def check_system_elements_in_state(self, num_edges, state):
        current_edges = 0
        exist_cloud = False

        while current_edges < num_edges or not exist_cloud:
            current_config = self.controller.get_complete_configuration()
            clients = self.controller.get_element_type_from_configuration(current_config, ElementType.CLIENT)
            for client in clients:
                if client.state == state:
                    current_edges += 1
            clouds = self.controller.get_element_type_from_configuration(current_config, ElementType.CLOUD)
            for cloud in clouds:
                if cloud.state == state:
                    exist_cloud = True
            time.sleep(WAITING_TIME)


def controller_main(master_ip, master_port, test_source):
    controller = Controller(master_ip, master_port)
    with open(test_source) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            controller.perform_test(model_name=row['model_name'],
                                    split_layer=int(row['split_layer']),
                                    num_images=int(row['num_images']),
                                    num_edges=int(row['num_edges']),
                                    edge_batch_size=int(row['edge_batch_size']),
                                    cloud_batch_size=int(row['cloud_batch_size']),
                                    no_repetitions=int(row['no_repetitions']))
            controller.reset_system()
    controller.stop_system()


if __name__ == '__main__':
    controller_main('localhost', 10100, './vgg19_test_configurations.csv')
