import flask.views

from ssum.view.exceptions import ViewNotFoundError

class ViewHandler:
    '''Class responsible for managing the view classes.'''

    __views: dict[str, type[flask.views.View]]

    def __init__(self):
        '''Store a dictionary of view classes from the views package.'''

        self.__views = {}

    def get_view(self, id: str) -> type[flask.views.View]:
        '''Return the view class with the given ID.
        If the ID doesn't match a view, raise ViewNotFoundError.'''

        try:
            return self.__views[id]
        except KeyError:
            raise ViewNotFoundError(
                f"No view with ID '{id}' was found!"
            )