
from datetime import datetime, timedelta

from sqlalchemy import Integer, ForeignKey, Enum
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from dateutil.relativedelta import relativedelta

from ssum.model.db import db
from ssum.model.duration_enum import DurationEnum
from ssum.model.models.timestamp_mixin import TimestampMixin

class Subscription(db.Model, TimestampMixin):
    '''One of the user's paid subscriptions.
    It has an optional relationship to the SubscriptionPreset it was created with.'''

    id = mapped_column(Integer(), primary_key=True)
    name = Mapped[str]
    price_in_pence = Mapped[int]
    duration = Enum(DurationEnum)

    # Optional relationship to the preset it was defined with.
    preset_id = mapped_column(ForeignKey("subscription_preset.id"))

    # This Relationship object allows the preset to be easily retrieved in Python.
    preset_obj = relationship(
        "SubscriptionPreset", uselist=False,
        back_populates="used_by"
    )

    # Also related to one of `SubscriptionPreset.tiers`.
    tier_id = mapped_column(ForeignKey("subscription_preset_tier.id"))
    tier_obj = relationship(
        "SubscriptionPresetTier", uselist=False,
        back_populates="used_by"
    )

    @hybrid_property
    def next_renewal(self) -> datetime:
        '''Return the next time this subscription needs renewing.'''

        now = datetime.now()

        # Use the relativedelta class to account for leap years
        # and differing amounts of days in a month.
        match (self):
            case DurationEnum.WEEK: return now + timedelta(weeks=1)
            case DurationEnum.YEAR: return now + relativedelta(years=1)
            case _: return now + relativedelta(months=1)