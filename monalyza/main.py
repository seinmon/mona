import sys
from monitoring import monitoring


if __name__ == '__main__':
    process = sys.argv[1]

    try: 
        monitor = monitoring.Monitoring(process,
                                        interval=1,
                                        buffer_size=12000000)

    except ProcessLookupError as p_err:
        print(repr(p_err))
        quit(1)
        
    else:
        monitor.run(True, True)

