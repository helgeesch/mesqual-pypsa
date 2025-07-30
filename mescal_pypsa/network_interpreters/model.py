from typing import TYPE_CHECKING
from shapely import Point, LineString
import pandas as pd

from mescal_pypsa.network_interpreters.base import PyPSAInterpreter
from mescal.energy_data_handling.model_handling.membership_property_enrichers import (
    MembershipPropertyEnricher,
    DirectionalMembershipPropertyEnricher, MembershipTagging,
)
from mescal.energy_data_handling.model_handling.membership_pairs_appender import StringMembershipPairsAppender
from mescal.utils.geo_utils.geo_from_string import convert_wkt_series

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
            # TODO: handle multilinks with bus2, bus3, bus4, ...
            df = self.from_to_membership_enricher.append_properties(df, self.parent_dataset, MembershipTagging.PREFIX)
            df = self.from_to_pairs_as_str_appender.append_combo_columns(df)
            df = self.from_to_pairs_as_str_appender.append_sorted_combo_columns(df)
            df = self.from_to_pairs_as_str_appender.append_opposite_combo_columns(df)
            if flag in ['lines', 'links']:
                if 'geometry' not in df.columns:
                    df.loc[:, 'geometry'] = None

                def _get_linestring(o: pd.Series) -> LineString | None:
                    if o.geometry is not None:
                        return o.geometry
                    if not all(i in o for i in ['bus_location0', 'bus_location1']):
                        return None
                    if isinstance(o['bus_location0'], Point) and isinstance(o['bus_location1'], Point):
                        return LineString([o['bus_location0'], o['bus_location1']])
                    return None

                df.loc[:, 'geometry'] = df.apply(_get_linestring, axis=1)

            if flag == 'transformers':
                if 'location' not in df.columns:
                    df.loc[:, 'location'] = None

                def _get_location(o: pd.Series) -> Point | None:
                    if 'bus_location0' in o and isinstance(o['bus_location0'], Point):
                        return o['bus_location0']
                    if 'bus_location1' in o and isinstance(o['bus_location1'], Point):
                        return o['bus_location1']
                    return None

                df.loc[:, 'location'] = df.apply(_get_location, axis=1)

        elif 'bus' in df.columns:
            df = self.membership_prop_enricher.append_single_membership_properties(
                df,
                self.parent_dataset,
                membership_column='bus',
                membership_tagging=MembershipTagging.PREFIX
            )

        if 'geometry' in df.columns and is_all_string_or_empty(df['geometry']):
            df['geometry'] = convert_wkt_series(df['geometry'])

        return df


def is_all_string_or_empty(series: pd.Series) -> bool:
    return series.apply(lambda x: isinstance(x, str) or pd.isna(x) or x == "").all()
