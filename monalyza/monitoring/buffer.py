import csv
import logging
from os import confstr, getpid
from monalyza.monitoring import single_process_monitoring as spm


class Buffer:
    
    def __init__(self, buffer_size, output_file):
        logging.debug('Initializing buffer.')
        self.output_file = output_file
        self.data = [] 
        self.buffer_monitoring = spm.SingleProcessMonitoring(getpid()) 
        self.buffer_size = buffer_size

    def total_data(self, new_data):
        """ Add the measurements of all subprocesses every second """

        last_data_index = len(self.data)
        calculated_data = new_data

        logging.debug('Ready to calculate total data.')
        if (not isinstance(new_data[0], str)) and last_data_index > 0:
            logging.debug('Looking for entries in the buffer.')

            if self.data[last_data_index][0] / 1000 == new_data[0] / 1000:
                logging.debug('Modifying last element in buffer')
                calculated_data = self.data.pop()

                for index, entry in enumerate(new_data):
                    if index == 0:
                        continue

                    else:
                        calculated_data[index] += entry

        return calculated_data

    def append_to_buffer(self, data):
        logging.debug('Appending to buffer.')
        self.data.append(self.total_data(data))

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

