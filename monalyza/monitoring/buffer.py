from os import getpid
from . import monitoring


class Buffer:
    
    def __init__(self, buffer_size):
        self.data = dict()
        self.self_monitoring = monitoring.Monitoring(getpid(), interval=1) 
        self.buffer_size = buffer_size

    def append_to_buffer(self, column_title, data):
        if column_title in self.data:
            self.data[column_title].append(data)

        else:
            self.data[column_title] = [data]

        print(self.data[column_title])

        # TODO: Check memory for this process and write to data frame, then append to a csv file

