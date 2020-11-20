from flask import Blueprint
from flask_socketio import emit as single_emit
from server import socketio, redisc, GRID_HEIGHT, GRID_WIDTH
from server.util import change_colors, update_clients
import logging

log = logging.getLogger('server.socketio')

socketio_bp = Blueprint('socketio', __name__)

# receive light change command from client
@socketio.on("client_update_light")
def change_lights_message(message):
    log.info("Change Lights: " + str(message))

    # change colors on MQTT
    topic = "{:03d}".format(int(message['id']))
    # change_colors(topic, message["color"])

    update_clients(message['id'], message['color'])   

# debug channel
@socketio.on("info")
def print_debug(message):
    log.debug("Client Debug: " + str(message))

# when client connects to site
@socketio.on("connect")
def on_connect():
    redisc.incr('clients')
    log.info("Socket connected! Currently connected clients: {}".format(redisc.get('clients')))
    # for light in grid_list:
    #     print(light)

    # send the newly connected client the current color statuses
    for i in range(GRID_WIDTH*GRID_HEIGHT):
        message = {"id": i, "color": redisc.get(i)}
        single_emit("server_update_light", message)
        

@socketio.on("disconnect")
def on_disconnect():
    redisc.decr('clients')
    log.info("Client disconnected! Currently connected clients: {}".format(redisc.get('clients')))
