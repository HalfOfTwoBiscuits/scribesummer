from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from scribesummer.src.ssum.model.db import db
from scribesummer.src.ssum.model.interval_enum import IntervalEnum
from scribesummer.src.ssum.model.models.timestamp_mixin import TimestampMixin
from scribesummer.src.ssum.model.models.subscription_preset import SubscriptionPreset

class SubscriptionPresetTier(db.Model, TimestampMixin):
    '''A pre-populated tier for a subscription of a certain brand.
    Each SubscriptionPreset has one or more tiers.
    A subscription created with a preset can be switched around between tiers when editing.'''

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    price_in_pence: Mapped[int]
    interval: Mapped[IntervalEnum]

    # Relationship to the preset it is a tier of.
    preset_id: Mapped[str] = mapped_column(ForeignKey(SubscriptionPreset.id), nullable=False)

    preset_obj: Mapped["SubscriptionPreset"] = relationship( # type: ignore
        "SubscriptionPreset", uselist=False,
        back_populates="tiers"
    )

    used_by: Mapped[List["PresetBasedSubscription"]] = relationship( # type: ignore
        "PresetBasedSubscription",
        back_populates="tier_obj"
    )
