# Modbus Meter Emulator

Emulates an energy meter with modbus communication to enable export control on your inverter.
The project is intended to be used with Home Assistant, but can be used with any other system that supports MQTT and Modbus.

> [!CAUTION]
> This project is in the early phases of development. Please use with caution.
> I am not responsible for any damage caused by using this project.

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
poetry run meter <path-to-config-yaml>
```
Possitional arguments:
- `config`: Path to the configuration file.

Options:
- `-v` or `--verbose`: Enable verbose logging.
- `-h` or `--help`: Show help message.

> [!NOTE]
> If you get a weird error like `'format'` when running the command above, this is most likely because of the version of Poetry you are using.
> This project was developed with Poetry 1.8 and does not yet work with Poetry 2.0.
> Try running the tool with `poetry run python -m modbus_meter_emulator <path-to-config-yaml>`.

### Docker
This project is also available as a docker image.

#### Pull
```bash
docker pull ghcr.io/bossan/modbus-meter-emulator
```

#### Run
```commandline
docker run -v ./config.yaml:/etc/modbus-meter/config.yaml ghcr.io/bossan/modbus-meter-emulator
```

Where `./config.yaml` should be replaced with the location of your config file.

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
