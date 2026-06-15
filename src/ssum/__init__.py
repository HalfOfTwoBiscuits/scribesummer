from os import environ

from flask import Flask
from flask_migrate import Migrate

from ssum.controller import Controller
from ssum.model import ModelHandler
from ssum.view import ViewHandler
from ssum.config import EnvironmentVariableLoader, ConfigHandler
from ssum.config.exceptions import MissingEnvironmentVariableError

def create_app() -> Flask:
    '''Construct, configure, and return the app object.
    Uses either development or production configuration
    based on the `APP_CONFIG` environment variable.'''

    # Retrieve configuration from an environment variable.
    ch = ConfigHandler()
    CONFIG_ENVAR_NAME = "APP_CONFIG"

    try:
        config_name = environ[CONFIG_ENVAR_NAME]
        ConfigClass = ch.get_config(config_name)
    except KeyError:
        raise MissingEnvironmentVariableError(
            f"App configuration was not specified!\
            Please set the `{CONFIG_ENVAR_NAME}` environment variable\
            to one of: {ch.config_names}"
        )

    # Initialise app object.
    app = Flask(__name__)

    # Create environment variable loader.
    loader = EnvironmentVariableLoader(app)

    # Configure app object.
    config = ConfigClass(loader)
    config.configure()

    # Initialise app components.
    model_handler = ModelHandler(app)
    view_handler = ViewHandler()
    controller = Controller(app, model_handler, view_handler)
    controller.define_url_endpoints()

    # Initialise third-party app components.
    Migrate(app, model_handler.db, directory="ssum/migrations")

    return app