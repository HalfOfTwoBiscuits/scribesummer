
from datetime import datetime
from dateutil.relativedelta import relativedelta

from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.ext.hybrid import hybrid_method

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
    type: Mapped[str] # Indicates preset or custom.

    # This class is used as a polymorphic base,
    # meaning it is a table, but records are added only
    # through the children rather than directly.
    __mapper_args__ = {
        "polymorphic_on": "type",
        "polymorphic_abstract": True
    }

    first_renewal: Mapped[datetime]

    @hybrid_method
    def next_renewal(self, duration: IntervalEnum) -> datetime:
        '''Return the next time this subscription needs renewing.

        The renewal duration is passed as an argument,
        because depending on the child class it might be its own
        attribute or be determined by the preset subscription tier.'''

        # Starting from the first renewal,
        # repeatedly add the renewal duration
        # until the date is in the future.
        now = datetime.now()
        renewal = self.first_renewal
        while renewal < now:
            # Use the relativedelta class to account for leap years
            # and differing amounts of days in a month.
            match (duration.value):
                case IntervalEnum.WEEK: renewal += relativedelta(weeks=1)
                case IntervalEnum.YEAR: renewal += relativedelta(years=1)
                case _: renewal += relativedelta(months=1)

        return renewal
        