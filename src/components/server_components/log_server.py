import time
import os
import sys
import shutil
import pandas as pd
import numpy as np
from datetime import datetime
from src.utils.enums import get_thrift_enum_name

sys.path.append("gen-py")
from interfaces.ttypes import Message, PerformanceMessage, LogType, FileChunk, SpecsMessage




class LogServerInterfaceService:
    def __init__(self):
        base_path = "./logs/"
        if not os.path.exists(base_path):
            os.makedirs(base_path)
        else:
            shutil.rmtree(base_path)
            
        self.message_table = pd.DataFrame(columns=['timestamp', 'time', 'element_type', 'element_id', 'message'])
        self.message_file_path = base_path
        self.performance_table = pd.DataFrame(columns=['timestamp', 'time', 'element_type', 'element_id',
                                                       'no_images_predicted', 'list_ids', 'elapsed_time',
                                                       'decoded_ids', 'output_dimension'])
        self.performance_file_path = base_path
        self.specs_table = pd.DataFrame(columns=['timestamp', 'time', 'element_type','element_id'])
        self.specs_file_path = base_path

    def log_message(self, message: Message):
        new_row = pd.DataFrame([{'timestamp': message.timestamp,
                                 'time': str(datetime.fromtimestamp(message.timestamp)),
                                 'element_type': get_thrift_enum_name(message.element_type),
                                 'element_id': message.id,
                                 'message': message.message}])

        self.message_table = self.message_table.append(new_row, sort=False, ignore_index=True)

    def log_performance_message(self, message: PerformanceMessage):
        new_row = pd.DataFrame([{'timestamp': message.timestamp,
                                 'time': str(datetime.fromtimestamp(message.timestamp)),
                                 'element_type': get_thrift_enum_name(message.element_type),
                                 'element_id': message.id,
                                 'no_images_predicted': message.no_images_predicted,
                                 'list_ids': message.list_ids,
                                 'elapsed_time': message.elapsed_time,
                                 'decoded_ids': message.decoded_ids,
                                 'output_dimension': message.output_dimension}])

        self.performance_table = self.performance_table.append(new_row, sort=False, ignore_index=True)

        print(self.performance_table)

    def log_specs_message(self, message: SpecsMessage):
        if not (self.specs_table['element_id'] == message.id).any():
            new_row = pd.DataFrame([{'timestamp': message.timestamp,
                                     'time': str(datetime.fromtimestamp(message.timestamp)),
                                     'element_type': get_thrift_enum_name(message.element_type),
                                     'element_id': message.id}])
            self.specs_table = self.specs_table.append(new_row, sort=False, ignore_index=True)
        if message.spec not in self.specs_table:
            self.specs_table[message.spec] = np.nan
        elif pd.notna(self.specs_table.loc[self.specs_table['element_id'] == message.id, [message.spec]].values.take(0)):
            message.spec = message.spec + "_opt"
            self.specs_table[message.spec] = np.nan
        self.specs_table.loc[self.specs_table['element_id'] == message.id, [message.spec]] = message.value
        print(self.specs_table)

    def prepare_log(self, log_type: LogType):
        print("Preparing a log")
        if log_type == LogType.MESSAGE:
            self.message_file_path = "./logs/message_log_"+\
                                     str(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))+".csv"
            self.message_table.to_csv(self.message_file_path, encoding='utf-8', index=False)
            self.message_table = pd.DataFrame()
            print("Writing Messages")

        if log_type == LogType.PERFORMANCE:
            self.performance_file_path = "./logs/performance_log_"+\
                                         str(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))+".csv"
            self.performance_table.to_csv(self.performance_file_path, encoding='utf-8', index=False)
            self.performance_table = pd.DataFrame()
            print("Writing Performance")

        if log_type == LogType.SPECS:
            self.specs_file_path = "./logs/specs_log_"+\
                                   str(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))+".csv"
            self.specs_table.to_csv(self.specs_file_path, encoding='utf-8', index=False)
            print("Writing Specs")

    def get_log_chunk(self, log_type: LogType, offset: int, size: int):
        if log_type is LogType.MESSAGE:
            reader = open(self.message_file_path, "rb")
        elif log_type is LogType.PERFORMANCE:
            reader = open(self.performance_file_path, "rb")
        elif log_type is LogType.SPECS:
            reader = open(self.specs_file_path, "rb")

        reader.seek(offset)
        data = reader.read(size)
        current_position = reader.tell()
        reader.seek(0, 2)

        return FileChunk(data, remaining=reader.tell()-current_position)
