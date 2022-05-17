from __future__ import annotations
import logging
import time
from typing import TYPE_CHECKING
import psutil
from monalyza.monitoring import scheduler


if TYPE_CHECKING:
    from monalyza.monitoring.buffer import Buffer


class SingleProcessMonitoring:
    """Monitor a single process without its children."""

    def __init__(self,
                 pid: int,
                 interval: float = None,
                 buffer: 'Buffer' = None,
                 hide_headers: bool = False) -> None:
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
        """Measure resource consumption of a specific process repeatedly."""
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
        """Measure resource consumption of a specific process."""
        resource_info = None

        try:
            process = psutil.Process(self.pid)
            time = self.generate_timestamp()

            if read_memory and read_cpu:
                resource_info = (time[0],
                                 time[1],
                                 process.pid,
                                 process.memory_info()[0],
                                 process.cpu_percent(interval=0.1),
                                 process.status())

            elif read_memory:
                resource_info = (time[0],
                                 time[1],
                                 process.pid,
                                 process.memory_info()[0],
                                 process.status())

            elif read_cpu:
                resource_info = (time[0],
                                 time[1],
                                 process.pid,
                                 process.cpu_percent(interval=1),
                                 process.status())

        except psutil.NoSuchProcess:
            logging.error('Process %s no longer exists.', self.pid)
            raise

        else:
            return resource_info

    def generate_timestamp(self) -> tuple:
        """Get time and time difference in seconds, since initial time."""
        current_time = int(time.time())

        if self.initial_start_time == 0:
            self.initial_start_time = current_time

        return (current_time - self.initial_start_time, current_time)
