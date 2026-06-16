from abc import ABC
from datetime import datetime
from pathlib import Path
import logging

from flask.logging import wsgi_errors_stream

from ssum.config import EnvironmentVariableLoader

class BaseConfig(ABC):
    '''Base class for the objects responsible for
    configuring the app to suit either development or production.'''
    
    _loader: EnvironmentVariableLoader

    def __init__(
        self,
        loader: EnvironmentVariableLoader
    ):
        self._loader = loader

    def configure(self):
        '''Apply configuration values used in both development and production.
        To be called by children using `super()`.'''

        self._configure_logging()

        get = self._loader.get_config
        require = self._loader.require_config
        
        # Cryptographic secrets
        require("SECRET_KEY", str)

        # Database connection string
        require("SQLALCHEMY_DATABASE_URI", str)

    def _configure_logging(self):
        '''Configure logging for the app object.
        Logs go to the terminal, and also a file named after the
        current configuration and timestamp.
        Can be overriden to use different methods of logging.'''

        # Create logging directory if not present.
        log_dir_path = Path("logs").resolve()
        log_dir_path.mkdir(parents=True, exist_ok=True)

        # Determine filename of log file.
        timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M")
        log_file_path = log_dir_path / f"{self.__class__.__name__}-{timestamp}.log"

        # Configure logging.
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        )
        
        # Log to both a file, and the configured output stream, the terminal.
        file_handler = logging.FileHandler(filename=log_file_path)
        file_handler.setFormatter(formatter)
        
        wsgi_handler = logging.StreamHandler(stream=wsgi_errors_stream) # type: ignore
        wsgi_handler.setFormatter(formatter)

        logger = logging.getLogger('app')
        logger.addHandler(file_handler)
        logger.addHandler(wsgi_handler)

        log_level = self._logging_level()
        logger.setLevel(log_level)

    def _logging_level(self) -> str:
        '''Log level for the app.
        Can be overriden to change log level without altering logging method.'''

        return 'INFO'  