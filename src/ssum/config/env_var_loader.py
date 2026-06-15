from os import environ
from typing import Callable, TypeVar, Any

import flask

from ssum.config.exceptions import MissingEnvironmentVariableError

T = TypeVar("T")
D = TypeVar("D")

class EnvironmentVariableLoader:
    '''Utility class that loads configuration values
    from environment variables.'''

    __app: flask.Flask
    
    def __init__(self, app: flask.Flask):
        self.__app = app

    def get_config(self, name: str, datatype: Callable[[str], T]=str, default: D=None) -> T | D:
        '''Get a configuration value from the
        environment variable with the given name,
        and cast it to the given datatype.
        Set it on the app object.
        Finally, return it.

        If the variable isn't set, fall back to the given default.
        If default=None, then no value will be set.'''

        value = self.get_environ_var(name, datatype, default)

        if value is None:
            self.__app.logger.warning(
                "No environment variable or default value was provided "
                f"for the config value: `{name}`"
            )

        self.__set(name, value)
        return value

    def require_config(self, name: str, datatype: Callable[[str], T]=str) -> T:
        '''Get a configuration value from the
        environment variable with the given name,
        and cast it to the given datatype.
        Set it on the app object.
        Finally, return it.

        If the variable isn't set, 
        raise MissingEnvironmentVariableError.'''
        
        value = self.require_environ_var(name, datatype)
        self.__set(name, value)
        return value

    def require_environ_var(self, name: str, datatype: Callable[[str], T]=str) -> T:
        '''Return the value of the environment variable
        with the given name, cast to the given datatype.

        If the variable isn't set, 
        raise MissingEnvironmentVariableError.'''
        
        try: 
            value = environ[name]
        except KeyError:
            raise MissingEnvironmentVariableError(
                f"Required environment variable `{name}` is missing.\
                Please set it in the `.env` file before deploying the app."
            )

        return datatype(value)

    def get_environ_var(self, name: str, datatype: Callable[[str], T]=str, default: D=None) -> T | D:
        '''Return the value of the environment variable
        with the given name, cast to the given datatype.

        If the variable isn't set, fall back to the given default.'''

        try:
            value = environ[name]
        except KeyError:
            if default is not None:
                self.__app.logger.info(
                    f"Environment variable `{name}` is not present, "
                    f"so we use the provided default, `{default}`."
                )
            return default
        else:
            return datatype(value)

    def __set(self, name: str, value: Any):
        '''Utility method to set a configuration value.'''

        self.__app.config[name] = value