from server import create_app, socketio
import os

app = create_app(debug=True)

if __name__ == '__main__':
    socketio.run(app, port=os.environ['PORT'], host='0.0.0.0')