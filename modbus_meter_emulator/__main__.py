import argparse
import threading
import logging

from modbus_meter_emulator import Config, ModbusServer, MqttClient
from modbus_meter_emulator.meters import create_meter_from_config


logger = logging.getLogger('modbus_meter_emulator')


parser = argparse.ArgumentParser(
    prog='Modbus Meter Emulator',
    description='Emulates an energy meter with modbus communication.',
    epilog='Created by: Sander Bos https://github.com/bossan'
)

parser.add_argument(
    'config',
    metavar='config',
    type=str,
    help='Path to the configuration file'
)

parser.add_argument(
    '-v',
    '--verbose',
    action='store_true',
    help='Enable verbose logging'
)

args = parser.parse_args()

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.DEBUG if args.verbose else logging.INFO
)

config = Config(args.config)

meter = create_meter_from_config(meter_config=config.meter)

modbus_server = ModbusServer(modbus_config=config.modbus, meter=meter)
mqtt_client = MqttClient(mqtt_config=config.mqtt, topics=meter.get_topics(), on_update_hook=meter.set_data)

modbus_thread = threading.Thread(target=modbus_server.run)
mqtt_thread = threading.Thread(target=mqtt_client.run)

modbus_thread.daemon = True
mqtt_thread.daemon = True

try:
    modbus_thread.start()
    mqtt_thread.start()
    modbus_thread.join()
    mqtt_thread.join()
except KeyboardInterrupt:
    logger.info("Exiting...")
    exit(0)
