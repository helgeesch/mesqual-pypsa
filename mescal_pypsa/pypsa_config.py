from dataclasses import dataclass

from mescal.datasets import DatasetConfig


@dataclass
class PyPSADatasetConfig(DatasetConfig):
    only_accept_non_empty_timeseries: bool = False  # whether you want to include empty time-series in accepted_flags
