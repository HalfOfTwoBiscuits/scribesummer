from scribesummer.src.ssum.config.configs.base_config import BaseConfig
from scribesummer.src.ssum.config.configs.development_config import DevelopmentConfig
from scribesummer.src.ssum.config.configs.production_config import ProductionConfig

class ConfigNotFoundError(Exception): pass

class ConfigHandler:
    '''Class responsible for managing the config classes.'''

    __configs: dict[str, type[BaseConfig]]

    def __init__(self):
        '''Store a dictionary of view classes from the views package.'''

        self.__configs = {"development": DevelopmentConfig, "production": ProductionConfig}

    @property
    def config_names(self) -> list[str]:
        '''Names of config classes.
        Valid values for the APP_CONFIG environment variable.'''
        
        return list(self.__configs.keys())

    def get_config(self, id: str) -> type[BaseConfig]:
        '''Return the view class with the given ID.
        If the ID doesn't match a view, raise ViewNotFoundError.'''

        try:
            return self.__configs[id]
        except KeyError:
            raise ConfigNotFoundError(
                f"No view with ID '{id}' was found!"
            )