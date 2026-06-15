import flask_wtf

class FormNotFoundError(Exception): pass

class FormHandler:

    __forms: dict[str, type[flask_wtf.FlaskForm]]

    def __init__(self):
        '''Store a dictionary of form classes from the forms package.'''

        self.__forms = {}

    def get_form(self, id: str) -> type[flask_wtf.FlaskForm]:
        '''Return the form class with the given ID.
        If the ID doesn't match a form, raise FormNotFoundError.'''

        try:
            return self.__forms[id]
        except KeyError:
            raise FormNotFoundError(
                f"No form with ID '{id}' was found!"
            )