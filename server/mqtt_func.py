from flask import Blueprint
from server import mqtt, redisc
from server.util import update_clients, create_subscribers
import logging

log = logging.getLogger('server.mqtt')

mqtt_bp = Blueprint('mqtt', __name__)


@mqtt.on_connect()
def mqtt_connect_cb(client, userdata, flags, rc):
    log.info("MQTT Connected!")
    width = int(redisc.get('grid_width'))
    height = int(redisc.get('grid_height'))
    
    create_subscribers(width, height)

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    log.info("Received message! [{}]: {}".format(message.topic, message.payload.decode()))
    update_clients(message.topic, message.payload.decode())