import csv
import logging
from os import getpid
from monalyza.monitoring import single_process_monitoring as spm


class Buffer:
    
    def __init__(self, buffer_size, output_file):
        logging.debug('Initializing buffer.')
        self.output_file = output_file
        self.data = [] 
        self.buffer_monitoring = spm.SingleProcessMonitoring(getpid()) 
        self.buffer_size = buffer_size

    def append_to_buffer(self, data):
        logging.debug('Appending to buffer.')
        self.data.append(data)

        if self.buffer_monitoring.read_resource(
            read_memory=True)[1] > self.buffer_size:
                logging.debug('Writing to file.')
                self.write_data()
                

    def write_data(self):
        with open(self.output_file, 'a+') as csv_output:
            if self.data:
                writer = csv.writer(csv_output)
                writer.writerows(self.data)
                self.data.clear()
                logging.debug('Buffer is cleared.')

