import abc
from typing import List, Any

from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext


class BaseMeter(abc.ABC):
    """
    Base class for all meters. All meters should inherit from this class.
    """

    CONFIG_TYPE = None

    _config: CONFIG_TYPE = None
    _context: ModbusServerContext = None

    def __init__(self, config: dict):
        self._set_config(config)
        self._context = ModbusServerContext(slaves=ModbusSlaveContext(
            di=ModbusSequentialDataBlock.create(),
            co=ModbusSequentialDataBlock.create(),
            hr=ModbusSequentialDataBlock.create(),
            ir=ModbusSequentialDataBlock.create()
        ), single=True)
        self.set_initial_data()

    def _set_config(self, config: dict):
        self._config = self.CONFIG_TYPE(**config)

    @property
    def context(self) -> ModbusServerContext:
        return self._context

    @abc.abstractmethod
    def set_initial_data(self):
        raise NotImplementedError

    @abc.abstractmethod
    def set_data(self, topic: str, payload: Any):
        raise NotImplementedError

    @abc.abstractmethod
    def get_topics(self) -> List[str]:
        raise NotImplementedError
