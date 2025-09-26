from typing import Type

from pypsa import Network

from mesqual.datasets import PlatformDataset, Dataset
from mesqual.databases import Database
from mesqual.utils.logging import get_logger

from mesqual_pypsa.network_interpreters.base import PyPSAInterpreter
from mesqual_pypsa.pypsa_config import PyPSADatasetConfig
from mesqual_pypsa.pypsa_flag_index import PyPSAFlagIndex

logger = get_logger(__name__)


class PyPSADataset(PlatformDataset[Dataset, PyPSADatasetConfig, str, PyPSAFlagIndex]):
    def __init__(
            self,
            network: Network,
            name: str = None,
            attributes: dict = None,
            database: Database = None,
            config: PyPSADatasetConfig = None,
    ):
        if name is None and network.name is None:
            logger.info(f'No name passed ')
        super().__init__(
            name=name or network.name or f'{PyPSADataset.__name__}_{str(id(self))}',
            flag_index=self.get_flag_index_type()(self),
            attributes=attributes,
            database=database,
            config=config,
            network=network,
        )
        self.n = network

    @classmethod
    def get_flag_type(cls) -> Type[str]:
        return str

    @classmethod
    def get_flag_index_type(cls) -> type[PyPSAFlagIndex]:
        return PyPSAFlagIndex

    @classmethod
    def get_config_type(cls) -> type[PyPSADatasetConfig]:
        return PyPSADatasetConfig

    @classmethod
    def get_child_dataset_type(cls) -> type[PyPSAInterpreter]:
        return PyPSAInterpreter

    @classmethod
    def _register_core_interpreters(cls):
        from mesqual_pypsa.network_interpreters.model import PyPSAModelInterpreter
        from mesqual_pypsa.network_interpreters.time_series import PyPSATimeSeriesInterpreter
        from mesqual_pypsa.network_interpreters.objective import PyPSAObjectiveInterpreter

        cls.register_interpreter(PyPSAModelInterpreter)
        cls.register_interpreter(PyPSATimeSeriesInterpreter)
        cls.register_interpreter(PyPSAObjectiveInterpreter)


PyPSADataset._register_core_interpreters()
