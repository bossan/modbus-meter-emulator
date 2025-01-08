from .base import BaseMeter
from .debug import DebugMeter
from .solax import SolaxMeter
from ..shared.config import MeterType


def create_meter_from_config(meter_config: MeterType) -> BaseMeter:
    """
    Factory function to return the correct meter class based on the meter name.
    """

    if meter_config.type == "solax":
        return SolaxMeter(meter_config.config)
    elif meter_config.type == "debug":
        return DebugMeter(meter_config.config)
    else:
        raise ValueError(f"Meter {meter_config.type} not supported")


__all__ = ["create_meter_from_config", "BaseMeter", "DebugMeter", "SolaxMeter"]
