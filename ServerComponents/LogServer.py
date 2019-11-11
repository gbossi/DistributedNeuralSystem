from ttypes import Message, PerformanceMessage
import time, queue
from utils.enums import get_thrift_enum_name
import pandas as pd


# cartelle
#   -Hardware: NomeMacchina
#       -Applicazione: CNN
#           -Configurazione: rete // Dimensione dati // numero-campioni taglio
#                  -Timestamp:
#                       -Ripetizione:
#                              Dump info relativo hardware

class LogServerInterfaceService:
    def __init__(self):
        self.messageQueue = queue.Queue()
        self.message_table = pd.DataFrame()

        self.performanceQueue = queue.Queue()
        self.performance_table = pd.DataFrame()



    def log_message(self, message: Message):
        self.messageQueue.put(message)
        new_row = pd.DataFrame([{'time': time.localtime(message.timestamp),
                                 'server_type': get_thrift_enum_name(message.server_type),
                                 'element_id': message.id,
                                 'message': message.message}])

        self.message_table = self.message_table.append(new_row)

        print(self.message_table)


    def log_performance_message(self, message: PerformanceMessage):
        self.performanceQueue.put(message)
        print(time.asctime(time.localtime(message.timestamp)),
              get_thrift_enum_name(message.server_type),
              message.id,
              message.no_images_predicted,
              message.list_ids,
              message.elapsed_time)



