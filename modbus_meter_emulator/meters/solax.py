import logging
from typing import List, Any

from pydantic import BaseModel
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadBuilder

from .base import BaseMeter


logger = logging.getLogger(__name__)


class SolaxMeterConfigType(BaseModel):
    current_power_state_topic: str
    energy_import_state_topic: str
    energy_export_state_topic: str


class SolaxMeter(BaseMeter):
    """
    Class for Solax meters. Inherits from BaseMeter.
    """

    CONFIG_TYPE = SolaxMeterConfigType

    DATA_MAP = {
        'import/export': {
            'topic': None,
            'opp': 0x10,
            'address': 40,
            'w_order': Endian.LITTLE,
            'b_order': Endian.BIG,
            'value_type': '32bit_int',
            'value_formatter': lambda x: int(float(x) * 10)
        },
        'total_import': {
            'topic': None,
            'opp': 0x10,
            'address': 62,
            'w_order': Endian.LITTLE,
            'b_order': Endian.BIG,
            'value_type': '32bit_int',
            'value_formatter': lambda x: int(float(x) * 10)
        },
        'total_export': {
            'topic': None,
            'opp': 0x10,
            'address': 92,
            'w_order': Endian.LITTLE,
            'b_order': Endian.BIG,
            'value_type': '32bit_int',
            'value_formatter': lambda x: int(float(x) * 10)
        }
    }

    def __init__(self, config: dict):
        super().__init__(config)
        self.DATA_MAP['import/export']['topic'] = self._config.current_power_state_topic
        self.DATA_MAP['total_import']['topic'] = self._config.energy_import_state_topic
        self.DATA_MAP['total_export']['topic'] = self._config.energy_export_state_topic

    def get_topics(self) -> List[str]:
        return [
            self._config.current_power_state_topic,
            self._config.energy_import_state_topic,
            self._config.energy_export_state_topic
        ]

    def set_initial_data(self):
        logger.debug("Setting initial data for SolaxMeter")
        self.context[0x00].setValues(0x06, 11, [71])  # Meter ID
        self.context[0x00].setValues(0x06, 14, [0, 0])  # Current consumption?
        self.context[0x00].setValues(0x10, 40, [0, 0])  # Import/export
        self.context[0x00].setValues(0x10, 62, [0, 0])  # Total import
        self.context[0x00].setValues(0x10, 92, [0, 0])  # Total export

    def set_data(self, topic: str, data: Any):
        data_map = None

        # Get the data map that contains the topic
        for key, value in self.DATA_MAP.items():
            if value['topic'] == topic:
                data_map = value
                break

        if data_map is None:
            return

        formatted_data = data_map['value_formatter'](data)
        builder = BinaryPayloadBuilder(wordorder=data_map['w_order'], byteorder=data_map['b_order'])
        getattr(builder, f'add_{data_map["value_type"]}')(formatted_data)
        logger.debug(f"Setting data for SolaxMeter: {data_map['opp']} {data_map['address']} {builder.to_registers()}")
        self.context[0x00].setValues(data_map['opp'], data_map['address'], builder.to_registers())
