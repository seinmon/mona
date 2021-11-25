import sys
from monitoring import monitoring


if __name__ == '__main__':
    proc_name = sys.argv[1]

    try: 
        monitor = monitoring.Monitoring(1, proc_name)
    except ProcessLookupError as p_err:
        print(repr(p_err))
        quit(1)
        
    else:
        monitor.run(False, True)
