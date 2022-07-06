from __future__ import annotations
from os import path
import sys
import logging
import argparse
from mona.core import proc, buffer
import mona.core.recursive_monitoring as rcm
import mona.core.single_process_monitoring as spm


def initialize_logger(level: int = logging.DEBUG,
                      verbose_print: bool = True) -> None:
    """
    Initialize logger with the specified logging level.

    - Parameters:
        -- level = in integer regresenting the level of logging, default value
        is logging.DEBUG
        -- verpose_print: print logs while executing, default value is True
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
    parser = argparse.ArgumentParser(prog="Mona")

    # General command line arguments:
    parser.add_argument('--version', action='version',
                        version='%(prog)s 0.0.1')
    parser.add_argument('--verbose', action='store_true',
                        help='print logs to to console')
    parser.add_argument('--logging-level', type=int,
                        help='the level logged messages from 0 (not set),\
                        to 5 (critical)')
    return parser


def start_monitoring(command: str | int,
                     read_memory: bool = True,
                     read_cpu: bool = True,
                     recursive: bool = True,
                     interval: float = 1,
                     output: str = 'measurements_output.csv',
                     buffer_size: int = 12000000,
                     recursion_time: int | None = None,
                     recursion_interval: float = 0.01) -> int:
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
        -- recursion_time: currently not implemented -- duration of
        searching for subprocesses
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

    else:
        if recursive:
            monitor = rcm.RecursiveMonitoring(pid, output_buffer,
                                              interval=interval,
                                              recursion_time=recursion_time,
                                              recursion_interval=
                                              recursion_interval)
            monitor.start()

        else:
            monitor = spm.SingleProcessMonitoring(pid, interval=interval,
                                                  buffer=output_buffer)
            monitor.run_repeatedly(read_memory, read_cpu)

        return 0


def main() -> int:
    """
    Starting point of the application.

    - Returns: exit status
    """
    # args = initialize_argparse().parse_args()
    # initialize_logger(level=args['logging-level'] * 10,
    #                   verbose_print=args['verbose'])
    
    initialize_logger()
    logging.info('Starting...')
    command = sys.argv[1]

    if (len(sys.argv) > 2):
        return start_monitoring(command, output=sys.argv[2])

    return start_monitoring(command)
