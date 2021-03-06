from flask import Flask
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_redis import FlaskRedis
import eventlet
import os, sys, eventlet, logging

eventlet.monkey_patch()

mqtt = Mqtt(connect_async=True, mqtt_logging=True)
socketio = SocketIO()
redisc = FlaskRedis(charset="utf-8", decode_responses=True)

def create_app():
    app = Flask(__name__)
    app.config['MQTT_BROKER_URL'] = os.getenv("MQTT_BROKER_URL")  
    app.config['MQTT_BROKER_PORT'] = int(os.getenv("MQTT_PORT"))
    app.config['MQTT_USERNAME'] = os.getenv("MQTT_USER")  
    app.config['MQTT_PASSWORD'] = os.getenv("MQTT_PASSWD")   
    app.config['MQTT_KEEPALIVE'] = 30  # set the time interval for sending a ping to the broker to 30 seconds
    app.config['MQTT_TLS_ENABLED'] = False  # set TLS to disabled for testing purposes
    app.config['MQTT_CLIENT_ID'] = os.getenv("MQTT_CLIENT_ID")
    app.config['REDIS_URL'] = os.getenv("REDIS_URL")
    
    app.debug = os.getenv("DEBUG")

    # have to set this manually because it wont work through app.config for some reason
    mqtt.client_id = os.getenv("MQTT_CLIENT_ID")

    app.logger.info("app config set")

    # register blueprints
    with app.app_context():
        app.logger.info("registering blueprints...")
        from server.mqtt_func import mqtt_bp 
        from server.socketio_func import socketio_bp 
        from server.main import main_bp

        app.register_blueprint(main_bp)
        app.register_blueprint(mqtt_bp)
        app.register_blueprint(socketio_bp)
        app.logger.info("done registering!")

    # init mqtt and socketio
    app.logger.info("initializing libraries...")
    redisc.init_app(app)
    socketio.init_app(app, async_mode='eventlet')
    app.logger.info("done initializing!")
    mqtt.init_app(app)  

    # init beginning board + connections num
    redisc.set('clients', 0)
    if int(redisc.exists('grid_width')) < 1 or int(redisc.exists('grid_height')) < 1:
        redisc.set('grid_width', 3)
        redisc.set('grid_height', 3)

    return app
