from datetime import date

from wtforms.validators import ValidationError, StopValidation

def category_ids_match(message: str):
    '''For each ID in the provided field, get the matching category record.
    If any IDs don't match, validation fails.'''
    
    def validator(form, field):
        for cat_id in field.data:
            cat = form.db.session.get(form.CategoryModel, cat_id)

            if cat is None:
                raise StopValidation(message)

    return validator

def date_in_future(message):
    '''Validator which checks the given date is in the future.'''
    
    def validator(form, field):
        if (date.today() - field.data).days > 0:
            raise ValidationError(message)
    
    return validator

def validate_box_checked(message):
    '''Validates that at least one box was checked on the MultiCheckboxField
    by raising an error if len() of the data is 0.
    This could potentially be done with the built-in Length validator,
    but the documentation says it is for strings so I elected not to stretch its use case.'''

    def validator(form, field):
        if len(field.data) == 0:
            raise ValidationError(message)
    
    return validator