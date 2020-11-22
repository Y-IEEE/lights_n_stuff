from flask import Blueprint
from flask_socketio import emit as single_emit
from server import socketio, redisc
from server.util import change_colors, update_clients, reset_grid, get_topic_from_index
import logging

log = logging.getLogger('server.socketio')

socketio_bp = Blueprint('socketio', __name__)

# receive light change command from client
@socketio.on("client_update_light")
def change_lights_message(message):
    log.info("Change Lights: " + str(message))

    # TODO will enable this when relevant
    # change colors on MQTT 
    # width = int(message['width'])
    # height = int(message['height'])
    # topic = get_topic_from_index(message['id'])
    # change_colors(topic, message["color"])

    update_clients(message['id'], message['color'])  

@socketio.on("client_dim_submit")
def change_grid_dims(message):
    log.info("Changing grid dims: [{}, {}]".format(message['width'], message['height']))

    width = int(message['width'])
    height = int(message['height'])

    redisc.set('grid_width', width)
    redisc.set('grid_height', height)

    # GLOBAL EMIT to all connected clients with the new dimensions
    socketio.emit("create_grid", {'width': width, 'height': height})
    reset_grid(width, height)
    
    

# debug channel
@socketio.on("info")
def print_debug(message):
    log.debug("Client Debug: " + str(message))

# when client connects to site
@socketio.on("connect")
def on_connect():
    redisc.incr('clients')
    log.info("Socket connected! Currently connected clients: {}".format(redisc.get('clients')))

    width = int(redisc.get('grid_width'))
    height = int(redisc.get('grid_height'))

    # create the grid
    single_emit("create_grid", {'width': width, 'height': height})
    
    # send the newly connected client the current color statuses
    for i in range(width*height):
        light_id = get_topic_from_index(i, width, height)
        message = {"id": light_id, "color": redisc.get(light_id)}
        single_emit("server_update_light", message)
        

@socketio.on("disconnect")
def on_disconnect():
    redisc.decr('clients')
    log.info("Client disconnected! Currently connected clients: {}".format(redisc.get('clients')))
