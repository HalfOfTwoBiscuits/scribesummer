
from datetime import datetime
from dateutil.relativedelta import relativedelta

from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property

from scribesummer.src.ssum.model.db import db
from scribesummer.src.ssum.model.interval_enum import IntervalEnum
from scribesummer.src.ssum.model.models.timestamp_mixin import TimestampMixin

class Subscription(db.Model, TimestampMixin):
    '''One of the user's paid subscriptions.
    
    This is the base class for
    SubscriptionFromPreset and CustomSubscription.

    Unlike those, it is a table in the database.
    This class is the table,
    and the children specify specific attributes.'''

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(255)) # Indicates preset or custom.

    # This class is used as a polymorphic base,
    # meaning it is a table, but records are added only
    # through the children rather than directly.
    __mapper_args__ = {
        "polymorphic_on": "type",
        "polymorphic_abstract": True
    }

    first_renewal: Mapped[datetime]

    @hybrid_property
    def next_renewal(self) -> datetime:
        '''Return the next time this subscription needs renewing.'''

        # Attribute will always be present, since this is a child.
        interval = self.interval # type: ignore

        # Starting from the first renewal,
        # repeatedly add the renewal duration
        # until the date is in the future.
        now = datetime.now()
        renewal = self.first_renewal
        while renewal < now:
            # Use the relativedelta class to account for leap years
            # and differing amounts of days in a month.
            match (interval.value): 
                case IntervalEnum.WEEK: renewal += relativedelta(weeks=1)
                case IntervalEnum.YEAR: renewal += relativedelta(years=1)
                case _: renewal += relativedelta(months=1)

        return renewal
    
    @hybrid_property
    def monthly_price_in_pence(self) -> int:
        '''Return price in pence converted to a monthly interval.'''

        # Attributes will always be present, since this is a child.
        price_in_pence = self.price_in_pence # type: ignore
        interval = self.interval # type: ignore

        match (interval.value):
            case IntervalEnum.WEEK: price_in_pence *= 4
            case IntervalEnum.YEAR: price_in_pence //= 12
        return price_in_pence

    @hybrid_method
    def price_string(self, always_monthly: bool=False) -> str:
        '''Readable representation of the subscription's price.
        If always_monthly=True it will use the monthly interval,
        overriding the subscription's actual interval.'''

        # If always monthly, convert interval.
        if always_monthly:
            price_in_pence = self.monthly_price_in_pence
            interval = IntervalEnum.MONTH
        else:
            # Attributes will always be present, since this is a child.
            price_in_pence = self.price_in_pence # type: ignore
            interval = self.interval # type: ignore

        # Get price string.
        PENCE_IN_POUND = 100

        pounds = price_in_pence // PENCE_IN_POUND
        pence = price_in_pence - pounds * PENCE_IN_POUND
        if pence < 10:
            price_string = f'£{pounds}.0{pence}'
        else:
            price_string = f'£{pounds}.{pence}'

        return f"{price_string}/{interval.name.lower()}"