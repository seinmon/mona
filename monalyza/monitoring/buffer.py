from os import getpid
from . import monitoring


class Buffer:
    
    def __init__(self, buffer_size):
        self.data = [] 
        self.buffer_monitoring = monitoring.Monitoring(getpid(), interval=1) 
        self.buffer_size = buffer_size

    def append_to_buffer(self, data):
        self.data.append(data)

        print(self.data)

        if self.buffer_monitoring.read_resource(
            read_memory=True)[1] > self.buffer_size:
            self.write_data()

    def write_data(self):
        pass

