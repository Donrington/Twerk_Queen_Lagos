from main import app
from flask_socketio import SocketIO

socketio = SocketIO(app)

if __name__ == "__main__":
    # This is okay for local testing only
    socketio.run(app, debug=False)
