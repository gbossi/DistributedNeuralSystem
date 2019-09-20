from interfaces import ImageLoader
from interfaces import ttypes
from thrift_servers import Server
import numpy as np
import os, random, queue
from PIL import Image


class ImageLoaderService:
    def __init__(self, img_directory):
        self.data = None
        self.image_iterator = self.build_iterator(img_directory)

    def get_image(self):
        path = self.image_iterator.get()
        img_file = Image.open(path)
        img_data = np.array(img_file)
        img_data_type = img_data.dtype.name
        img_shape = img_data.shape
        if self.image_iterator.empty():
            last = True
        else:
            last = False
        return ttypes.Image(img_data.tobytes(), img_data_type, img_shape, last)

    @staticmethod
    def build_iterator(img_directory):
        image_queue = queue.Queue()
        file_names = [item for item in os.listdir(img_directory)]
        file_paths = []
        for file_name in file_names:
            file_paths = file_paths+[os.path.join(img_directory, file_name)]
        random.shuffle(file_paths)
        for file_path in file_paths:
            image_queue.put(file_path)
        return image_queue


if __name__ == '__main__':
    image_path = "./images/"
    service = ImageLoaderService(image_path)
    print("Starting python server...")
    processor = ImageLoader.Processor(service)
    server = Server(processor, port=40400)
    server.serve()
    print("done!")
