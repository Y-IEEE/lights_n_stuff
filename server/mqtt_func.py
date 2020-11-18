from flask import Blueprint
# from flask import current_app as app
from server import mqtt 
from server import GRID_HEIGHT, GRID_WIDTH
from server.util import update_clients


mqtt_bp = Blueprint('mqtt', __name__)

def create_subscribers(width, height):
    for i in range(width*height):
        topic = "{:03d}".format(i)
        mqtt.subscribe(topic)

@mqtt.on_connect()
def mqtt_connect_cb(client, userdata, flags, rc):
    app.logger.error("MQTT Connected!")
    create_subscribers(GRID_WIDTH, GRID_HEIGHT)

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    app.logger.debug("Received message! [{}]: {}".format(message.topic, message.payload.decode()))
    update_clients(message.topic, message.payload.decode())