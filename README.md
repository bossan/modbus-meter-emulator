# Modbus Meter Emulator

Emulates an energy meter with modbus communication. The project is intended to be used with Home Assistant, but can be
used with any other system that supports MQTT and Modbus.

> [!CAUTION]
> This project is in the early phases of development. Please use with caution.

## Installation

The current version uses [Poetry](https://python-poetry.org).
Install the project and dependencies with:

```bash
poetry install
```

## Configuration

Example:

```yaml
mqtt:
  broker:
    host: homeassistant.local
    port: 1883
    username: ha-user
    password: password
    keepalive: 60

modbus:
  port: "/dev/ttyUSB0"
  baudrate: 9600
  bytesize: 8
  parity: N
  stopbits: 1

meter:
  type: solax
  config:
    current_power_state_topic: "homeassistant/sensor/p1_meter_power/state"
    energy_import_state_topic: "homeassistant/sensor/p1_meter_energy_import/state"
    energy_export_state_topic: "homeassistant/sensor/p1_meter_energy_export/state"
```

## Usage

Run the project with:

```bash
poetry run python -m modbus_meter_emulator <path-to-config-yaml>
```

## Supported Inverters

| Brand | Model     | Tested             | Notes                                                                      |
|-------|-----------|--------------------|----------------------------------------------------------------------------|
| Solax | X3 MIC G2 | :white_check_mark: | Current import/export is working, still need to validate the other values. |

## Credits

Used the following repo's for inspiration:

- [syssi/esphome-solax-x1-mini](https://github.com/syssi/esphome-solax-x1-mini/).
- [wills106/homeassistant-solax-modbus](https://github.com/wills106/homeassistant-solax-modbus)
- [straga/Smart-Meter-Gateway](https://github.com/straga/Smart-Meter-Gateway)

And huge thanks
to [raenji-sk/Solax-X3-MIC-G2-Virtual-Smart-Meter](https://github.com/raenji-sk/Solax-X3-MIC-G2-Virtual-Smart-Meter) for
basically sorting out all the used addresses, so I don't have to.
