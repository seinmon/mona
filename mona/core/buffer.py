from __future__ import annotations
import csv
import logging
from os import getpid
from typing import TYPE_CHECKING
from mona.core import monitoring


if TYPE_CHECKING:
    from typing import Any


class Buffer:
    """Write the measurements to a csv file, once a threshold is reached."""

    def __init__(self, buffer_size: int, output_file: str) -> None:
        """
        Write the measurements to a csv file, once a threshold is reached

        - Parameters:
            -- buffer_size: size of the buffer in bytes
            -- output_file: address of the file to write the data when clearing
            the buffer
        """
        logging.debug('Initializing buffer.')
        self.output_file = output_file
        self.data = []
        self.buffer_monitoring = monitoring.Monitoring(getpid())
        self.buffer_size = buffer_size

    def append_to_buffer(self, data: Any) -> None:
        """
        Add data to the buffer, and write to csv file if it is necessary

        Modules that want to use buffer should only use append_to_buffer
        method. Other methods are to be used within the buffer itself.

        - Parameters:
            -- data: the data to add to the buffer
        """
        logging.debug('Appending to buffer.')
        self.data.append(data)

        used_buffer = self.buffer_monitoring.read_resource(read_memory=True)
        if used_buffer is not None:
            if used_buffer[1] > self.buffer_size:
                logging.debug('Writing to file.')
                self.write_data()

    def write_data(self) -> None:
        """Writes data to file, and clears the buffer"""
        with open(self.output_file, 'a+', encoding='UTF-8') as csv_output:
            if self.data:
                writer = csv.writer(csv_output)
                writer.writerows(self.data)
                self.data.clear()
                logging.debug('Buffer is cleared.')
