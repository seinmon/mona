from __future__ import annotations
from os import path
import logging
import argparse
from mona.core import proc, buffer, monitoring
import mona.core.recursive_monitoring as rcm


def initialize_logger(level: int = logging.DEBUG,
                      verbose_print: bool = False) -> None:
    """
    Initialize logger with the specified logging level.

    - Parameters:
        -- level = logging level, defaults to logging.DEBUG
        -- verpose_print: print logs while executing, default value is False
    """
    logging.basicConfig(
        filename=path.join(path.expanduser('~'), '.mona.log'),
        encoding='utf-8',
        level=level,
        format='%(asctime)s [%(levelname)s]'
        '[%(threadName)s/%(thread)d] %(message)s')

    if verbose_print:
        logging.getLogger().addHandler(logging.StreamHandler())


def initialize_argparse() -> argparse.ArgumentParser:
    """
    Initialize argparse

    - Returns: an instance of argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser(prog='Mona')

    parser.add_argument('process',
                        help='PID or the name of the process to profile')

    parser.add_argument('-i', '--interval', type=float, default=0.9,
                        help='time interval of sampling resource values')

    parser.add_argument('--cpu', action='store_true',
                        help='measure CPU consumption')

    parser.add_argument('--memory', action='store_true',
                        help='measure memory consumption')

    parser.add_argument('-o', '--output', type=str,
                        default='measurements_output.csv',
                        help='Address of the measurements file')

    parser.add_argument('-b', '--buffer-size', type=int, default=12000000,
                        help='Size of the buffer (in bytes)')

    parser.add_argument('-r', '--recursive', action='store_true',
                        help='look up subprocesses and profile them as well')

    parser.add_argument('-ri', '--recursive_with_interval', type=float,
                        default=0.1, help='recursive profiling, with interval\
                        for looking up subprocesses')

    parser.add_argument('-v', '--verbose', action='store_true',
                        help='print logs to to console')

    parser.add_argument('-l', '--logging-level', type=int,
                        choices=[1, 2, 3, 4, 5], default=4,
                        help='the level of logged messages from 1 (all logs) \
                        to 5 (critical logs only).')

    parser.add_argument('--version', action='version',
                        version='%(prog)s 0.0.1', help='Print version number')

    return parser


# I added default values to the function, in case in was used without argparse
# pylint: disable-next=too-many-arguments
def start_monitoring(command: str | int,
                     read_memory: bool = True,
                     read_cpu: bool = True,
                     recursive: bool = True,
                     interval: float = 1,
                     output: str = 'measurements_output.csv',
                     buffer_size: int = 12000000,
                     recursion_interval: float = 0.1) -> int:
    """
    Start monitoring with the selected configuration options

    - Parameters:
        -- process: pid or name of the target process
        -- read_memory: set true to monitor memory, default value is True
        -- read_cpu: set true to monitor cpu, default value is True
        -- recursive: set true to monitor subprocesses of the target process,
        default value is True
        -- interval: inteval of repeating measurements in seconds, default
        value is 1
        -- output: address of the output file, defaults  value is
        measurements_output.csv
        -- buffer_size: size of the buffered measurements in bytes, default
        value is 12000000 bytes
        -- recursion_interval: interval of searching for subprocesses in
        seconds, default value is 0.1

    - Returns: exit status
    """
    output_buffer = buffer.Buffer(buffer_size, output)

    try:
        pid = proc.get_pid_of_process(command)

    except ProcessLookupError as p_err:
        logging.error(repr(p_err))
        return 1

    if recursive:
        mona = rcm.RecursiveMonitoring(pid, output_buffer,
                                       interval=interval,
                                       recursion_interval=recursion_interval)
        mona.start()

    else:
        mona = monitoring.Monitoring(pid, interval=interval,
                                     buffer=output_buffer)
        mona.run_repeatedly(read_memory, read_cpu)

    return 0


def main() -> int:
    """
    Starting point of the application.

    - Returns: exit status
    """
    args = initialize_argparse().parse_args()
    initialize_logger(level=args.logging_level * 10,
                      verbose_print=args.verbose)

    logging.info('Starting...')

    if not (args.cpu or args.memory):
        args.cpu = True
        args.memory = True

    if args.recursive_with_interval:
        args.recursive = True

    return start_monitoring(
        args.process, read_memory=args.memory, read_cpu=args.cpu,
        recursive=args.recursive, interval=args.interval, output=args.output,
        buffer_size=args.buffer_size,
        recursion_interval=args.recursive_with_interval
    )
