from __future__ import annotations
import sys
import matplotlib.pyplot as plt
# from monalyza.analysis import loader
from loader import Loader


def plot(x_title: str, y_title: str, measurements: str,
         output: str = 'plot.png'):
    loader = Loader(measurements)
    plt.plot(loader.get_column(x_title), loader.get_column(y_title))
    plt.savefig(output)


if __name__ == '__main__':
    plot('step', 'cpu', sys.argv[1], 'cpu_'+sys.argv[2]+'.png')
    plot('step', 'memory', sys.argv[1], 'memory_'+sys.argv[2]+'.png')
