from typing import List

from sqlalchemy.orm import mapped_column, Mapped, relationship

from ssum.model.db import db
from ssum.model.models.timestamp_mixin import TimestampMixin
from ssum.model.models.category_joins import category_for_preset
from ssum.model.models.subscription_preset_tier import SubscriptionPresetTier
from ssum.model.models.category import Category
from ssum.model.models.preset_based_subscription import PresetBasedSubscription

class SubscriptionPreset(db.Model, TimestampMixin):
    '''A pre-populated preset for a subscription of a certain brand.'''

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]

    # Available tiers for this preset.
    tiers: Mapped[List[SubscriptionPresetTier]] = relationship(
        SubscriptionPresetTier,
        back_populates="preset_obj"
    )

    categories: Mapped[List[Category]] = relationship(
        Category,
        secondary=category_for_preset,
        back_populates="presets_using_it"
    )

    used_by: Mapped[List[PresetBasedSubscription]] = relationship(
        PresetBasedSubscription,
        back_populates="preset_obj"
    )