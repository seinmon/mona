import sys
from monitoring import monitoring


if __name__ == '__main__':
    proc_name = sys.argv[1]
    monitor = monitoring.Monitoring(1, proc_name)
    monitor.memory()
