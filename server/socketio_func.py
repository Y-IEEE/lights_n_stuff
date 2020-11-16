from flask import Blueprint
from flask import current_app as app
from server import socketio
from server.util import change_colors

bp = Blueprint('socketio', __name__)


def update_clients(light_id, val):
    app.logger.debug("Updating clients...: ({}, {})".format(light_id, val))
    message = {"id": light_id, "color": val}
    socketio.emit("server_update_light", message, json=True) # broadcast=true not needed for socketio.emit

# receive light change command from client
@socketio.on("client_update_light")
def change_lights_message(message):
    app.logger.debug("Change Lights: " + str(message))

    # change colors on MQTT
    change_colors(message["id"], message["color"])

    # update internal light array, id = index which is really bad rn, find a better way of doing this
    # grid_list[int(message['id'])].set_color(message['color'])
    update_clients(message['id'], message['color'])   

# debug channel
@socketio.on("info")
def print_debug(message):
    print("Client Debug: " + str(message))

# when client connects to site
@socketio.on("connect")
def on_connect():
    app.logger.debug("Socket connected!")
    # for light in grid_list:
    #     print(light)

    # # send the newly connected client the current color statuses
    # for node in grid_list:
    #     update_clients(node.get_id(), node.get_color())

@socketio.on("disconnect")
def on_disconnect():
    app.logger.debug("Client disconnected!")
