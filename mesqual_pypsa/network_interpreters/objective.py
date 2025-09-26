from typing import TYPE_CHECKING

import pandas as pd

from mesqual_pypsa.network_interpreters.base import PyPSAInterpreter

if TYPE_CHECKING:
    from mesqual_pypsa.pypsa_config import PyPSADatasetConfig


class PyPSAObjectiveInterpreter(PyPSAInterpreter):
    @property
    def accepted_flags(self) -> set[str]:
        return {'objective'}

    def _required_flags_for_flag(self, flag: str) -> set[str]:
        return set()

    def _fetch(self, flag: str, effective_config: 'PyPSADatasetConfig', **kwargs) -> pd.Series | pd.DataFrame:
        return pd.Series(
            {
                'objective': self.n.objective,
                'objective_constant': self.n.objective_constant
            }
        )
