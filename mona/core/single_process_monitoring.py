from __future__ import annotations
import logging
import time
from typing import TYPE_CHECKING
import psutil
from mona.core import scheduler


if TYPE_CHECKING:
    from mona.core.buffer import Buffer


class SingleProcessMonitoring:
    """Monitor a single process without its children."""

    def __init__(self,
                 pid: int,
                 interval: float | None = None,
                 buffer: 'Buffer' | None  = None,
                 hide_headers: bool = False) -> None:
        """
        Monitor a single process without its children

        - Parameters:
            -- pid: pid of the target process
            -- interval: interval of repeating the measurements, default value
            is None
            -- buffer: an instance of buffer to be used for writing the data,
            default value is None
            hide_headers: set to true if measuring subprocesses, default value
            is True
        """
        self.initial_start_time = 0
        self.pid = pid
        self.first_run = not hide_headers

        logging.debug('Initializing single process monitoring.')
        self.buffer = buffer

        if interval is not None:
            self.scheduler = scheduler.Scheduler(interval)

        else:
            self.scheduler = None

    def run_repeatedly(self, read_memory: bool = False,
                       read_cpu: bool = False) -> None:
        """
        Measure resource consumption of a specific process repeatedly

        - Parameters:
            -- read_memory: set to true to monitor memory consumption, defalt
            value is False
            -- read_cpu: set to true to monitor cpu consumption, defalt value
            is False
        """
        if self.scheduler is None or self.buffer is None:
            raise UnboundLocalError(
                'Unexpectped value:',
                self.buffer,
                self.scheduler,
                'Either interval or buffer_size_mb is missing')

        try:
            resource_info = self.read_resource(read_memory, read_cpu)

        except psutil.NoSuchProcess:
            self.scheduler.cancel_scheduler()
            self.buffer.write_data()

        else:
            if self.first_run:
                headers = None

                if read_memory and read_cpu:
                    headers = ('step', 'time', 'pid', 'memory', 'cpu',
                               'status')

                elif read_memory:
                    headers = ('step', 'time', 'pid', 'memory', 'status')

                elif read_cpu:
                    headers = ('step', 'time', 'pid', 'cpu', 'status')

                self.buffer.append_to_buffer(headers)
                self.first_run = False

            self.buffer.append_to_buffer(resource_info)
            self.scheduler.schedule(self.run_repeatedly,
                                    read_memory=read_memory,
                                    read_cpu=read_cpu)

    def read_resource(self, read_memory: bool = False,
                      read_cpu: bool = False) -> tuple | None:
        """Measure resource consumption of a specific process

        - Parameters:
            -- read_memory: set to true to monitor memory consumption, defalts
            to False
            -- read_cpu: set to true to monitor cpu consumption, defalts to
            False

        - Returns: a tuple of measurement values, structured as below:
            (time since start, timestamp, pid, measurement...)

        - Raises:
            -- psutil.NoSuchProcess if the process does not exist anymore
        """
        resource_info = None

        try:
            process = psutil.Process(self.pid)
            timestamp = self.generate_timestamp()

            if read_memory and read_cpu:
                resource_info = (timestamp[0],
                                 timestamp[1],
                                 process.pid,
                                 process.memory_info()[0],
                                 process.cpu_percent(interval=0.1),
                                 process.status())

            elif read_memory:
                resource_info = (timestamp[0],
                                 timestamp[1],
                                 process.pid,
                                 process.memory_info()[0],
                                 process.status())

            elif read_cpu:
                resource_info = (timestamp[0],
                                 timestamp[1],
                                 process.pid,
                                 process.cpu_percent(interval=1),
                                 process.status())

        except psutil.NoSuchProcess:
            logging.error('Process %s no longer exists.', self.pid)
            raise

        else:
            return resource_info

    def generate_timestamp(self) -> tuple[int, int]:
        """
        Get time and time difference since start in seconds

        - Returns: a tuple of time since beginning of monitoring and timestamp.
        Time difference is at index 0, and timestamp is at index 1.
        """
        current_time = int(time.time())

        if self.initial_start_time == 0:
            self.initial_start_time = current_time

        return (current_time - self.initial_start_time, current_time)
