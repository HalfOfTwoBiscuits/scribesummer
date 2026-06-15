import flask
import flask_sqlalchemy.model

from ssum.model.db import db
from ssum.model.exceptions import ModelNotFoundError

class ModelHandler:
    '''Class responsible for setting up the SQLAlchemy database and storing its models.'''

    __models: dict[str, type[flask_sqlalchemy.model.Model]]

    def __init__(
        self,
        app: flask.Flask
    ):
        '''Initialise the database object and store the database model classes.'''
        
        db.init_app(app)
        self.__db = db
        self.__models = {}

    @property
    def db(self): 
        '''Return the database object.'''

        return self.__db

    def get_model(self, id: str) -> type[flask_sqlalchemy.model.Model]:
        '''Return the model with the given ID.
        If the ID doesn't match a model, raise ModelNotFoundError.'''

        try:
            return self.__models[id]
        except KeyError:
            raise ModelNotFoundError(
                f"No database model with ID '{id}' was found!"
            )