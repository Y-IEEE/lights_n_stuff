from server import mqtt

def change_colors(chip_id, color):
    mqtt.publish(str(chip_id), color)
    