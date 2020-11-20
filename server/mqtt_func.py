from flask import Blueprint
from server import GRID_HEIGHT, GRID_WIDTH, mqtt
from server.util import update_clients
import logging

log = logging.getLogger('server.mqtt')

mqtt_bp = Blueprint('mqtt', __name__)

def create_subscribers(width, height):
    for i in range(width*height):
        topic = "{:03d}".format(i)
        log.info("Subscribing to Topic: {}".format(topic))
        mqtt.subscribe(topic)

@mqtt.on_connect()
def mqtt_connect_cb(client, userdata, flags, rc):
    log.info("MQTT Connected!")
    create_subscribers(GRID_WIDTH, GRID_HEIGHT)

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    log.info("Received message! [{}]: {}".format(message.topic, message.payload.decode()))
    update_clients(message.topic, message.payload.decode())