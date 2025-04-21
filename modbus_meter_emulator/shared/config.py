from enum import Enum

import yaml
from typing import Optional
from pydantic import BaseModel
from pymodbus import FramerType


class MqttBrokerConfigType(BaseModel):
    host: str
    port: int
    username: Optional[str] = None
    password: Optional[str] = None
    keepalive: Optional[int] = 60


class MqttConfigType(BaseModel):
    broker: MqttBrokerConfigType


class ModbusConnectionType(str, Enum):
    TCP = 'tcp'
    SERIAL = 'serial'


class ModbusConfigType(BaseModel):
    connectionType: ModbusConnectionType = ModbusConnectionType.SERIAL
    address: Optional[str] = 'localhost'
    port: str  # /dev/tty... for serial or tcp port for tcp
    framer: Optional[FramerType] = FramerType.RTU
    stopbits: Optional[int] = 1
    bytesize: Optional[int] = 8
    parity: Optional[str] = 'N'
    baudrate: Optional[int] = 9600


class MeterType(BaseModel):
    type: str
    config: dict  # This needs to be validated by each meter implementation


class ConfigType(BaseModel):
    mqtt: MqttConfigType
    modbus: ModbusConfigType
    meter: MeterType


class Config:
    _config: ConfigType = None

    def __init__(self, config_path: str):
        with open(config_path, 'r') as yaml_file:
            config = yaml.safe_load(yaml_file)
            self._config = ConfigType(**config)

    @property
    def mqtt(self) -> MqttConfigType:
        return self._config.mqtt

    @property
    def modbus(self) -> ModbusConfigType:
        return self._config.modbus

    @property
    def meter(self) -> MeterType:
        return self._config.meter
