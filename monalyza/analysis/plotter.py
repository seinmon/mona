from __future__ import annotations
import sys
import matplotlib.pyplot as plt
# from monalyza.analysis import loader
from loader import Loader


def plot(x_title: str, x_metric: str, y_title: str, y_metric: str,
         measurements: str, x_func, y_func, output: str = 'plot.png'):
    loader = Loader(measurements)
    x_values = loader.get_column(x_title)
    y_values = loader.get_column(y_title)

    if x_func is not None:
        x_values = x_func(x_values)

    if y_func is not None:
        y_values = y_func(y_values)

    plt.plot(y_values)
    plt.savefig(output)


if __name__ == '__main__':
    plot('step', 'Seconds', 'cpu', 'percent', sys.argv[1], None, None, 'cpu_'+sys.argv[2]+'.png')

    f = lambda arr: [int(x / 1000000) for x in arr]
    plot('step', 'Seconds', 'memory', 'MB', sys.argv[1],  None, f,'memory_'+sys.argv[2]+'.png')
