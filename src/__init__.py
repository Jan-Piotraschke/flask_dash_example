from flask import Flask
import os
from flask_assets import Environment

def init_app():
    app = Flask(__name__, instance_relative_config=False, static_folder=os.path.abspath('src/static'), static_url_path='')
    app.config.from_object('config.Config')
    assets = Environment()
    assets.init_app(app)

    with app.app_context():
        # Import parts of our core Flask app
        from . import routes
        from .assets import compile_static_assets

        # Import Dash application
        from .dash.dashboard import init_dashboard
        app = init_dashboard(app)

        # Compile static assets
        compile_static_assets(assets)

        return app
