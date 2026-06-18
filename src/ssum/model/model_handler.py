import flask
import flask_sqlalchemy.model

from scribesummer.src.ssum.model.db import db
from scribesummer.src.ssum.model.pre_populator import PrePopulator
from scribesummer.src.ssum.model.exceptions import ModelNotFoundError
from scribesummer.src.ssum.model.models import Subscription, CustomSubscription, PresetBasedSubscription, SubscriptionPreset, SubscriptionPresetTier, Category, User

class ModelHandler:
    '''Class responsible for setting up the SQLAlchemy database and storing its models.
    It encapsulates access to the database object, model classes, and prepopulator,
    making them easy to integrate with other parts of the program such as
    views and terminal commands.'''

    __models: dict[str, type[flask_sqlalchemy.model.Model]]
    __prepopulator: PrePopulator

    def __init__(
        self,
        app: flask.Flask
    ):
        '''Initialise the database object and store the database model classes.'''
        
        db.init_app(app)
        self.__db = db

        # By using fixed identifiers, the class names can change
        # without affecting other parts of the program that use them.
        self.__models = {
            "Subscription": Subscription,
            "CustomSubscription": CustomSubscription,
            "PresetBasedSubscription": PresetBasedSubscription,
            "SubscriptionPreset": SubscriptionPreset,
            "SubscriptionPresetTier": SubscriptionPresetTier,
            "Category": Category,
            "User": User
        }

        self.__prepopulator = PrePopulator(db)

    @property
    def db(self): 
        '''Return the database object.'''

        return self.__db
    
    @property
    def prepopulator(self): 
        '''Return the prepopulator object.'''

        return self.__prepopulator

    def get_model(self, id: str) -> type[flask_sqlalchemy.model.Model]:
        '''Return the model with the given ID.
        If the ID doesn't match a model, raise ModelNotFoundError.'''

        try:
            return self.__models[id]
        except KeyError:
            raise ModelNotFoundError(
                f"No database model with ID '{id}' was found!"
            )