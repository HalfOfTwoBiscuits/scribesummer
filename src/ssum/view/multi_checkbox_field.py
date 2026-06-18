from wtforms import SelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput
from wtforms.validators import ValidationError

class MultiCheckboxField(SelectMultipleField):
    '''A field for selecting one or more elements using checkboxes.
    Used for subject selection.
    
    The native SelectMultipleField (<select multiple>) isn't the best since it
    requires desktop users to hold the control key when using it.
    Although I originally planned to get around this by rendering separate checkboxes using Jinja,
    to render them using WTForms I would have to add the checkbox fields in Python after the class is declared
    which would reduce maintainability since code would be distributed about unintuitively.

    Instead I took this simple solution from https://alexwlchan.net/til/2025/list-of-tickboxes-in-wtforms/
    which overrides the 'widget' objects used to render the SelectMultipleField in HTML.'''

    widget = ListWidget(prefix_label=True)
    option_widget = CheckboxInput()