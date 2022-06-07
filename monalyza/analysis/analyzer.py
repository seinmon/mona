from __future__ import annotations
import sys
import logging
from scipy import stats
# from monalyza.analysis import loader
import loader


class Analyzer:
    """Analyze the measurements."""

    def __init__(self, measurements: list[str]) -> None:
        self.data = []
        for entry in measurements:
            self.data.append(loader.Loader(entry))

    def measurements_are_valid(self, column: str) -> bool:
        """Validate measurements with Kruskal Wallis test."""
        logging.debug("Computing Kruskal Wallis")
        measurements = []
        for entry in self.data:
            measurements.append(entry.combine_and_get_column('time', column))

        return stats.kruskal(*measurements)[1] #> 0.05

if __name__ == '__main__':
    analyzer = Analyzer(sys.argv[1:])
    print('CPU:', analyzer.measurements_are_valid('cpu'))
    print('Memory', analyzer.measurements_are_valid('memory'))
