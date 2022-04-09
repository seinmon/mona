import logging
from scipy import stats
# from monalyza.analysis import loader
import loader


class Analyzer:
    def measurements_are_valid(self, *measurements: str) -> bool:
        """Validate measurements with Kruskal Wallis test."""
        logging.debug("Computing Kruskal Wallis")
        measurements = []

        for entry in measurements[0]:
            data = loader.Loader(entry)
            measurements.append(data.combine_and_get_column('time', 'cpu'))

        return stats.kruskal(*measurements)
