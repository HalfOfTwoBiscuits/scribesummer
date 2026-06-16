from typing import List

from sqlalchemy.orm import Mapped, relationship

from scribesummer.src.ssum.model.interval_enum import IntervalEnum
from scribesummer.src.ssum.model.models.base_subscription import Subscription
from scribesummer.src.ssum.model.models.category_joins import category_for_custom_sub

class CustomSubscription(Subscription):
    '''One of the user's paid subscriptions.
    Its attributes were specified manually by the user,
    without using a preset.
    
    This isn't a table in the database, its parent Subscription is.
    This class just specifies that the attributes are set directly,
    rather than using a relationship to a preset.

    SQLAlchemy calls this "Single Table Inheritance".
    See: https://docs.sqlalchemy.org/en/20/orm/inheritance.html'''

    name: Mapped[str]
    price_in_pence: Mapped[int]
    interval: Mapped[IntervalEnum]

    categories: Mapped[List["Category"]] = relationship( # type: ignore
        "Category",
        secondary=category_for_custom_sub,
        back_populates="custom_subscriptions_using_it"
    )

    # Its `type` attribute will be set to "custom".
    __mapper_args__ = {
        "polymorphic_identity": "custom"
    }