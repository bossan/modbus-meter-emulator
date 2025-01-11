import logging
import requests
from pymodbus.server import StartSerialServer

from modbus_meter_emulator.meters import BaseMeter
from modbus_meter_emulator.shared.config import ModbusConfigType


logger = logging.getLogger(__name__)


class ModbusServer:
    _modbus_config: ModbusConfigType = None
    _meter: BaseMeter = None

    def __init__(self, modbus_config: ModbusConfigType, meter: BaseMeter):
        self._modbus_config = modbus_config
        self._meter = meter

    def run(self):
        try:
            logger.info(f"Starting Modbus server on {self._modbus_config.port}...")
            StartSerialServer(
                context=self._meter.context,
                framer=self._modbus_config.framer,
                port=self._modbus_config.port,
                stopbits=self._modbus_config.stopbits,
                bytesize=self._modbus_config.bytesize,
                parity=self._modbus_config.parity,
                baudrate=self._modbus_config.baudrate,
            )
        except KeyboardInterrupt:
            logger.info("Exiting...")
            exit(0)
