"""Compile static assets."""
from flask import current_app as app


def compile_static_assets(assets):
    """
    Compile stylesheets if in development mode.
    :param assets: Flask-Assets Environment
    :type assets: Environment
    """
    assets.auto_build = True
    assets.debug = False
    return 