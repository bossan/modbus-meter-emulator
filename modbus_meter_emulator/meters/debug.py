import logging
from typing import List, Any
from pydantic import BaseModel
from pymodbus.datastore import ModbusServerContext, ModbusSlaveContext, ModbusSequentialDataBlock
from modbus_meter_emulator.meters import BaseMeter


logger = logging.getLogger(__name__)


class DebugMeterConfigType(BaseModel):
    pass


class CallbackDataBlock(ModbusSequentialDataBlock):
    """
    DataBlock with callback functions for getValues and set. Used for debugging purposes.
    """
    _name = ""
    _inc = 0

    def __init__(self, name, address, values):
        """Initialize the datastore with the requested values."""
        self._name = name
        super().__init__(address, values)

    def setValues(self, address, value):
        """Set the requested values of the datastore."""
        super().setValues(address, value)
        txt = f"Callback from setValues on {self._name} with address {address}, value {value}"
        logger.info(txt)

    def getValues(self, address, count=1):
        """Return the requested values from the datastore."""
        result = super().getValues(address, count)
        txt = f"Callback from getValues on {self._name} with address {address}, count {count}, data {result}"
        logger.info(txt)
        return result


class DebugMeter(BaseMeter):
    """
    Class for debugging purposes. Inherits from BaseMeter. Doesn't do anything useful other than print debug messages.
    """

    CONFIG_TYPE = DebugMeterConfigType

    def __init__(self, config: dict):
        self._set_config(config)
        di_block = CallbackDataBlock('di', 0x00, [0] * 100)
        co_block = CallbackDataBlock('co', 0x00, [0] * 100)
        hr_block = CallbackDataBlock('hr', 0x00, [0] * 100)
        ir_block = CallbackDataBlock('ir', 0x00, [0] * 100)

        self._context = ModbusServerContext(slaves=ModbusSlaveContext(
            di=di_block,
            co=co_block,
            hr=hr_block,
            ir=ir_block
        ), single=True)
        self.set_initial_data()

    def set_data(self, topic: str, data: Any):
        pass

    def get_topics(self) -> List[str]:
        return []

    def set_initial_data(self):
        pass
