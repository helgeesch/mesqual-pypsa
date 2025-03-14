from typing import TYPE_CHECKING
from shapely import Point
import pandas as pd

from mescal_pypsa.network_interpreters.base import PyPSAInterpreter
from mescal.energy_data_handling.model_handling.membership_property_enrichers import (
    MembershipPropertyEnricher,
    DirectionalMembershipPropertyEnricher, MembershipTagging,
)
from mescal.energy_data_handling.model_handling.membership_pairs_appender import StringMembershipPairsAppender

if TYPE_CHECKING:
    from mescal_pypsa.pypsa_config import PyPSADatasetConfig


class PyPSAModelInterpreter(PyPSAInterpreter):

    membership_prop_enricher = MembershipPropertyEnricher(membership_tag_separator='_')
    from_to_membership_enricher = DirectionalMembershipPropertyEnricher(
        from_identifier='0',
        to_identifier='1',
        membership_tag_separator='_',
    )
    from_to_pairs_as_str_appender = StringMembershipPairsAppender(
        from_identifier='0',
        to_identifier='1',
        combo_col_suffix='_combo',
        sorted_combo_col_suffix='_combo_sorted',
        opposite_combo_col_suffix='_combo_opposite'
    )

    @property
    def accepted_flags(self) -> set[str]:
        return set([c['list_name'] for k, c in self.n.components.items()])

    def _required_flags_for_flag(self, flag: str) -> set[str]:
        return set()

    def _fetch(self, flag: str, effective_config: 'PyPSADatasetConfig', **kwargs) -> pd.Series | pd.DataFrame:
        df = getattr(self.n, flag)
        if flag == 'buses':
            if 'x' in df.columns and 'y' in df.columns:
                df['location'] = df[['x', 'y']].apply(lambda x: Point(x.iloc[0], x.iloc[1]), axis=1)
        elif flag in ['lines', 'links', 'transformers']:
            df = self.from_to_membership_enricher.append_properties(df, self.parent_dataset, MembershipTagging.PREFIX)
            df = self.from_to_pairs_as_str_appender.append_combo_columns(df)
            df = self.from_to_pairs_as_str_appender.append_sorted_combo_columns(df)
            df = self.from_to_pairs_as_str_appender.append_opposite_combo_columns(df)
        elif 'bus' in df.columns:
            df = self.membership_prop_enricher.append_single_membership_properties(
                df,
                self.parent_dataset,
                membership_column='bus',
                membership_tagging=MembershipTagging.PREFIX
            )
        return df
