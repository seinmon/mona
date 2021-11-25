import sys
from monitoring import monitoring


if __name__ == '__main__':
    proc_name = sys.argv[1]

    try: 
        monitor = monitoring.Monitoring(proc_name, interval=1, buffer_size_mb=10)
    except ProcessLookupError as p_err:
        print(repr(p_err))
        quit(1)
        
    else:
        monitor.run(True, True)
