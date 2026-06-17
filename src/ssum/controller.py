import flask

from scribesummer.src.ssum.model import ModelHandler
from scribesummer.src.ssum.view import ViewHandler, FormHandler

class Controller:
    '''Class responsible for defining URL endpoints.'''

    __app: flask.Flask
    __mh: ModelHandler
    __vh: ViewHandler
    __fh: FormHandler

    def __init__(
        self,
        app: flask.Flask,
        model_handler: ModelHandler,
        view_handler: ViewHandler,
        form_handler: FormHandler
    ):
        '''Store the provided app, model handler, and view handler objects.'''
        
        self.__app = app
        self.__mh = model_handler
        self.__vh = view_handler
        self.__fh = form_handler

        with app.app_context():
            UserModel = self.__mh.get_model("User")
            self.__user = self.__mh.db.session.get(UserModel, 1)

    def define_url_endpoints(self):
        '''Configure the app to serve each page view at a
        corresponding URL endpoint.
        URL parameters, database models and forms that a view uses
        will be set up as arguments to the created view function.'''
        

    def __define_endpoint(self, class_name: str, url: str, *args):
        '''Utility method used to define an endpoint with the provided URL.
        The endpoint name will be the view class's name, converted to snake case.
        The arguments to `View.as_view()` will be the model handler, form handler, and user object, followed by *args.'''

        ViewClass = self.__vh.get_view(class_name)
        endpoint_name = self.__endpoint_name_for(class_name)

        self.__app.add_url_rule(
            url,
            view_func=ViewClass.as_view(
                endpoint_name, self.__mh, self.__fh, self.__user, *args
            )
        )

    def __endpoint_name_for(self, class_name: str) -> str:
        '''Utility method that converts the given name to snake case.
        Used to determine the name for an endpoint, which is used
        as an argument to the `flask.url_for()` method.'''

        name = ''
        for index, char in enumerate(class_name):
            if char.isalpha():
                if char.isupper() and index > 0:
                    name += '_'
                name += char.lower()
        return name