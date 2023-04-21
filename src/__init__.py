from flask import Flask
import os

def init_app():
    app = Flask(__name__, instance_relative_config=False, static_folder=os.path.abspath('src/static'), static_url_path='')
    app.config.from_object('config.Config')

    with app.app_context():
        # Import parts of our core Flask app
        from . import routes

        # Import Dash application
        from .dash.dashboard import init_dashboard
        app = init_dashboard(app)

        return app
