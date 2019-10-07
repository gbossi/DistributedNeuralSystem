from utils.thrift_servers import Server, ServerType
from interfaces import LogInterface, ttypes
import time, queue


class LogServerInterfaceService:
    def __init__(self):
        self.messageQueue = queue.Queue()

    def log_message(self, message: ttypes.Message):
        current_local_time = time.asctime(time.localtime(time.time()))
        self.messageQueue.put((current_local_time, message))
        print(current_local_time, message.server_type, message.id, message.message)


if __name__ == '__main__':
    service = LogServerInterfaceService()
    print("Starting python server...")
    processor = LogInterface.Processor(service)
    server = Server(ServerType.THREADED, processor, port=10100)

    server.serve()
    print("done!")