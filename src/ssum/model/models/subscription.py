from sqlalchemy import Integer, String, ForeignKey, Enum
from sqlalchemy.orm import mapped_column, Mapped, relationship

from ssum.model.db import db
from ssum.model.duration_enum import DurationEnum
from ssum.model.models.timestamp_mixin import TimestampMixin

class Subscription(db.Model, TimestampMixin):
    '''One of the user's paid subscriptions.
    It has an optional relationship to the SubscriptionPreset it was created with.'''

    id = mapped_column(Integer(), primary_key=True)
    name = mapped_column(String(length=255), nullable=False)
    price_in_pence = Mapped[int]
    duration = Enum(DurationEnum) # The due date can be retrieved from the duration enum.

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