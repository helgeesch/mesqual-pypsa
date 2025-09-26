from typing import TYPE_CHECKING

import pandas as pd

from mesqual_pypsa.network_interpreters.base import PyPSAInterpreter

if TYPE_CHECKING:
    from mesqual_pypsa.pypsa_config import PyPSADatasetConfig


class PyPSATimeSeriesInterpreter(PyPSAInterpreter):
    @property
    def accepted_flags(self) -> set[str]:
        accepted = set()
        only_accept_non_empty_timeseries = self.instance_config.only_accept_non_empty_timeseries
        for attr in dir(self.n):
            if attr.endswith('_t'):
                _dict_with_vars = getattr(self.n, attr)
                for var in _dict_with_vars.keys():
                    df = getattr(_dict_with_vars, var)
                    if not isinstance(df, pd.DataFrame):
                        continue
                    if not only_accept_non_empty_timeseries or not df.empty:
                        accepted.add(f'{attr}.{var}')
        return accepted

    def _required_flags_for_flag(self, flag: str) -> set[str]:
        return set()

    def _fetch(self, flag: str, effective_config: 'PyPSADatasetConfig', **kwargs) -> pd.Series | pd.DataFrame:
        component, var = flag.split('.')
        return getattr(getattr(self.n, component), var)
