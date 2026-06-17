from os import environ

from flask import Flask
from flask_migrate import Migrate

from scribesummer.src.ssum.controller import Controller
from scribesummer.src.ssum.model import ModelHandler
from scribesummer.src.ssum.view import ViewHandler, FormHandler
from scribesummer.src.ssum.config import EnvironmentVariableLoader, ConfigHandler
from scribesummer.src.ssum.config.exceptions import MissingEnvironmentVariableError

class AppFactory:
    '''Class responsible for initialising the app.'''

    __app: Flask
    __model_handler: ModelHandler
    __view_handler: ViewHandler
    __form_handler: FormHandler

    def __init__(self):
        '''Construct, configure, and store the app object.
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
        self.__app = Flask(__name__)

        # Create environment variable loader.
        loader = EnvironmentVariableLoader(self.__app)

        # Configure app object.
        config = ConfigClass(loader)
        config.configure()

        # Initialise app components.
        self.__model_handler = ModelHandler(self.__app)
        self.__view_handler = ViewHandler()
        self.__form_handler = FormHandler()
        controller = Controller(
            self.__app, self.__model_handler,
            self.__view_handler, self.__form_handler
        )
        controller.define_url_endpoints()

        # Initialise third-party app components.
        Migrate(self.__app, self.__model_handler.db, directory="ssum/migrations")

    @property
    def app(self) -> Flask:
        '''Return app object.'''
        
        return self.__app
    
    @property
    def model_handler(self) -> ModelHandler:
        '''Return model handler object.'''

        return self.__model_handler
    
    @property
    def view_handler(self) -> ViewHandler:
        '''Return view handler object.'''

        return self.__view_handler
    
    @property
    def form_handler(self) -> FormHandler:
        '''Return form handler object.'''

        return self.__form_handler