from ttypes import Message
import time, queue


class LogServerInterfaceService:
    def __init__(self):
        self.messageQueue = queue.Queue()

    def log_message(self, message: Message):
        current_local_time = time.asctime(time.localtime(message.timestamp))
        self.messageQueue.put(message)
        print(current_local_time, message.server_type, message.id, message.message)


