import logging
import time
import paho.mqtt.client as mqtt

from modbus_meter_emulator.shared.config import MqttConfigType


logger = logging.getLogger(__name__)


class MqttClient:
    _topics = []

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logger.info("Connected to MQTT broker")
            if len(self._topics) > 0:
                client.subscribe([(topic, 0) for topic in self._topics])
        else:
            logger.error(f"Connection failed with code {rc}")

    def on_message(self, client, userdata, message):
        if self._on_update_hook:
            self._on_update_hook(message.topic, message.payload.decode())

    def __init__(self, mqtt_config: MqttConfigType, topics, on_update_hook=None):
        self._topics = topics
        self._on_update_hook = on_update_hook

        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        broker = mqtt_config.broker
        self.client.username_pw_set(broker.username, broker.password)
        self.client.connect(broker.host, broker.port, broker.keepalive)

    def run(self):
        self.client.loop_start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Exiting...")
            self.client.disconnect()
            self.client.loop_stop()
            exit(0)
