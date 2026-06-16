from typing import List

from sqlalchemy.orm import mapped_column, Mapped, relationship

from scribesummer.src.ssum.model.db import db
from scribesummer.src.ssum.model.models.timestamp_mixin import TimestampMixin

class SubscriptionPreset(db.Model, TimestampMixin):
    '''A pre-populated preset for a subscription of a certain brand.'''

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]

    # Available tiers for this preset.
    tiers: Mapped[List["SubscriptionPresetTier"]] = relationship( # type: ignore
        "SubscriptionPresetTier",
        back_populates="preset_obj"
    )

    categories: Mapped[List["Category"]] = relationship( # type: ignore
        "Category",
        secondary="category_for_preset",
        back_populates="presets_using_it"
    )

    used_by: Mapped[List["PresetBasedSubscription"]] = relationship( # type: ignore
        "PresetBasedSubscription",
        back_populates="preset_obj"
    )