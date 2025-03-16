from flask import Flask
import stripe
from flask_socketio import SocketIO
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail

csrf = CSRFProtect()
mail = Mail()

def create_app():
    from main.models import db
    from main import user_routes, admin_routes  # Import routes here

    app = Flask(__name__, static_folder='static')
    app.config.from_pyfile("config.py", silent=True)
    app.config['JSON_AS_ASCII'] = False

    db.init_app(app)
    migrate = Migrate(app, db)
    socketio = SocketIO(app)
    csrf.init_app(app)
    mail.init_app(app)

    with app.app_context():
        user_routes.init_routes(app)  # Register user routes
        admin_routes.init_routes(app)  # Register admin routes

    return app, socketio

app, socketio = create_app()  # Ensure app is globally available