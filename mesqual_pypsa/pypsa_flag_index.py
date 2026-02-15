from mesqual.enums import ItemTypeEnum, VisualizationTypeEnum, TopologyTypeEnum
from mesqual.flag.flag_index import FlagIndex
from mesqual.units import Units
from mesqual.utils.logging import get_logger
from mesqual.utils.string_inflections import to_plural, to_singular

logger = get_logger(__name__)


class PyPSAFlagIndex(FlagIndex):
    VISUALIZATION_TYPE_MAPPING = {
        'bus': VisualizationTypeEnum.Point,
        'generator': VisualizationTypeEnum.Point,
        'load': VisualizationTypeEnum.Point,
        'transformer': VisualizationTypeEnum.Point,
        'line': VisualizationTypeEnum.Line,
        'link': VisualizationTypeEnum.Line,
        # TODO: add storage units, other object types
    }

    TOPOLOGY_TYPE_MAPPING = {
        'bus': TopologyTypeEnum.Node,
        'load': TopologyTypeEnum.NodeConnectedElement,
        'generator': TopologyTypeEnum.NodeConnectedElement,
        'transformer': TopologyTypeEnum.Edge,
        'line': TopologyTypeEnum.Edge,
        'link': TopologyTypeEnum.Edge,
        # TODO: add storage units, other object types
    }

    @classmethod
    def get_flag_type(cls) -> type[str]:
        return str

    def get_flag_from_string(self, flag_string: str) -> str:
        return flag_string

    def _get_linked_model_flag(self, flag: str) -> str:
        if self._get_item_type(flag) != ItemTypeEnum.TimeSeries:
            raise ValueError
        return flag.split('.')[0].replace('_t', '')

    def _get_item_type(self, flag: str) -> ItemTypeEnum:
        object_class = flag.split('.')[0]
        if object_class.endswith('_t'):
            return ItemTypeEnum.TimeSeries
        return ItemTypeEnum.Model

    def _get_visualization_type(self, flag: str) -> VisualizationTypeEnum:
        f = flag.lower()
        for k, t in self.VISUALIZATION_TYPE_MAPPING.items():
            if k in f:
                return t
        logger.warning(f'No VisualizationTypeEnum registered for {flag}. Falling back to "Other".')
        return VisualizationTypeEnum.Other

    def _get_topology_type(self, flag: str) -> TopologyTypeEnum:
        f = flag.lower()
        for k, t in self.TOPOLOGY_TYPE_MAPPING.items():
            if k in f:
                return t
        logger.warning(f'No TopologyTypeEnum registered for {flag}. Falling back to "Other".')
        return TopologyTypeEnum.Other

    def _get_unit(self, flag: str) -> Units.Unit:

        _mw_variables_contain = ['flow', 'trade_balance', '.p']
        if any(i in flag for i in _mw_variables_contain):
            return Units.MW

        _eur_per_mwh_contain = ['marginal_price']
        if any(i in flag for i in _eur_per_mwh_contain):
            return Units.EUR_per_MWh

        return Units.NaU

    def _get_linked_model_flag_for_membership_column(self, membership_column_name: str) -> str:
        return to_plural(membership_column_name)

    def _get_membership_column_name_for_model_flag(self, flag: str) -> str:
        return to_singular(flag.lower())
