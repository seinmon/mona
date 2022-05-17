from __future__ import annotations
import matplotlib.pyplot as plt
# from monalyza.analysis import loader
from loader import Loader


def plot(x_title: str, y_title: str, measurements: str,
         output: str = 'plot.png'):
    loader = Loader(measurements)
    plt.plot(loader.get_column(x_title), loader.get_column(y_title))
    plt.savefig(output)


if __name__ == '__main__':
    plot('step', 'cpu', 'measurements_output.csv', 'cpu_lineplot.png')
    plot('step', 'memory', 'measurements_output.csv', 'memory_lineplot.png')
