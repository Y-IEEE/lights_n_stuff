from server import mqtt, socketio, redisc
import logging

log = logging.getLogger('server.util')

def change_colors(chip_id, color):
    log.info("Sending MQTT message: {{topic: {}, message: {} }}".format(chip_id, color))
    mqtt.publish(str(chip_id), color)

# update all connected web clients with a grid update
def update_clients(light_id, val):
    log.info("Updating clients...: ({}, {})".format(light_id, val))
    message = {"id": light_id, "color": val}
    redisc.set(light_id, val)
    socketio.emit("server_update_light", message, json=True) # broadcast=true not needed for socketio.emit

# get the formatted topic string from an index in the grid and the grid's dimensions (e.g. '5' for 3x3 grid is 02x01)
def get_topic_from_index(i, width, height):
    i = int(i)
    x_num = i % width
    y_num = i // width
    return "{:02d}x{:02d}".format(x_num, y_num)
    
def create_subscribers(width, height):
    for i in range(width*height):
        topic = get_topic_from_index(i, width, height)
        log.info("Subscribing to Topic: {}".format(topic))
        mqtt.subscribe(topic)

# sets grid to white and re-creates subscribers
# TODO could be made more efficient by only subbing/unsubbing to topics that are needed?
def reset_grid(width, height):
    for i in range(width*height):
        # TODO need to set up a callback with this 
        # mqtt.unsubscribe_all()

        # subscribe to appropriate mqtt topic
        topic = get_topic_from_index(i, width, height)
        log.info("Subscribing to Topic: {}".format(topic))
        mqtt.subscribe(topic)

        # populate the board with white tiles
        message = {"id": topic, "color": "#ffffff"}
        redisc.set(topic, "#ffffff")
        socketio.emit("server_update_light", message)