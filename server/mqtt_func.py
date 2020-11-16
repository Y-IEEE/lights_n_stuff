from flask import Blueprint
from flask import current_app as app
from server import mqtt, GRID_HEIGHT, GRID_WIDTH

bp = Blueprint('mqtt', __name__)


def create_subscribers(width, height):
    for i in range(width*height):
        topic = "{:03d}".format(i)
        mqtt.subscribe(topic)

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    app.logger.debug("MQTT Connected!")
    create_subscribers(GRID_WIDTH, GRID_HEIGHT)

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    app.logger.debug("Received message! [{}]: {}".format(message.topic, message.payload.decode()))
    # update_clients(message.topic, message.payload.decode())