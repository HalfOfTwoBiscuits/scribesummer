from sqlalchemy import String, ForeignKey, Enum
from sqlalchemy.orm import mapped_column, Mapped, relationship

from ssum.model.db import db
from ssum.model.interval_enum import IntervalEnum
from ssum.model.models.timestamp_mixin import TimestampMixin

class SubscriptionPresetTier(db.Model, TimestampMixin):
    '''A pre-populated tier for a subscription of a certain brand.
    Each SubscriptionPreset has one or more tiers.
    A subscription created with a preset can be switched around between tiers when editing.'''

    id = mapped_column(String(length=255), primary_key=True)
    name = mapped_column(String(length=255), nullable=False)
    price_in_pence = Mapped[int]
    interval = Enum(IntervalEnum)

    # Relationship to the preset it is a tier of.
    preset_id = mapped_column(ForeignKey("subscription_preset.id"), nullable=False)
    preset_obj = relationship(
        "SubscriptionPreset", uselist=False,
        back_populates="tiers"
    )
