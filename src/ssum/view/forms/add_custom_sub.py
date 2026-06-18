from decimal import Decimal

from flask_wtf import FlaskForm
from wtforms import DecimalField, SubmitField, StringField, SelectField, SelectMultipleField, DateField
from wtforms.validators import DataRequired, NumberRange, AnyOf

from scribesummer.src.ssum.view.form_validators import category_ids_match, date_in_future

class AddCustomSubscriptionForm(FlaskForm):
    '''Form used to add a custom subscription.'''

    def __init__(self, mh, **kwargs):
        super().__init__(**kwargs)

        # Retrieve database object and models, for use in validation.
        self.__class__.db = mh.db
        self.__class__.Category = mh.get_model("Category")
        self.__class__.categories = []

    name = StringField("Name", [
        DataRequired("Please enter a name for the subscription.")
    ])

    categories = SelectMultipleField(
        "Categories",
        validators=[
            category_ids_match(
                "Some IDs you selected don't match a subscription category - "
                "please check all options are still selectable in the dropdown" \
                "after reloading the page, and all of them clearly relate " \
                "to a type of subscription."
            )
        ]
    )

    price = DecimalField(
        'Price',
        validators=[
            DataRequired("Please specify the price of the subscription."),
            NumberRange(
                min=0.01,
                message="The subscription's price must be positive."
            )
        ],
        default=Decimal(5),
        places=2
    )

    interval = SelectField(
        'per',
        # For some reason, pylance thinks I need a 'Choice' datatype here...
        choices=["Month", "Year", "Week"], # type: ignore
        validators=[
            DataRequired("Please specify the billing interval"),
            AnyOf(
                ["Month", "Year", "Week"],
                "Please specify a valid billing interval."
            )
        ]
    )

    date = DateField(
        'due on',
        validators=[
            DataRequired("Please specify the subscription's next due date."),
            date_in_future("The next due date of the subscription must be in the future.")
        ]
    )

    submit = SubmitField("+ Add to My Subscriptions")