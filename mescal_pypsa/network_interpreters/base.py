from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

from mescal.datasets import Dataset

from mescal_pypsa.pypsa_config import PyPSADatasetConfig
from mescal_pypsa.pypsa_flag_index import PyPSAFlagIndex

if TYPE_CHECKING:
    from pypsa import Network
    from mescal_pypsa.pypsa_dataset import PyPSADataset


class PyPSAInterpreter(Dataset[PyPSADatasetConfig, str, PyPSAFlagIndex], ABC):
    def __init__(self, network: 'Network', parent_dataset: 'PyPSADataset'):
        self.n = network
        name = (self.n.name or str(id(self))) + f' - {self.__class__.__name__}'
        super().__init__(name=name, parent_dataset=parent_dataset)

    @property
    def instance_config(self) -> PyPSADatasetConfig:
        return self._parent_dataset.instance_config

    @property
    def flag_index(self) -> PyPSAFlagIndex:
        return self._parent_dataset.flag_index

    @classmethod
    def get_config_type(cls) -> type[PyPSADatasetConfig]:
        return PyPSADatasetConfig

    @classmethod
    def get_flag_type(cls) -> type[str]:
        return str

    @classmethod
    def get_flag_index_type(cls) -> type[PyPSAFlagIndex]:
        return PyPSAFlagIndex
