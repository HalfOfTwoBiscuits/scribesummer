from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from ssum.model.db import db
from ssum.model.models.timestamp_mixin import TimestampMixin
from ssum.model.models.category_joins import category_for_preset

class SubscriptionPreset(db.Model, TimestampMixin):
    '''A pre-populated preset for a subscription of a certain brand.'''

    id = mapped_column(String(), primary_key=True)
    name = Mapped[str]

    # Available tiers for this preset.
    tiers = relationship(
        "SubscriptionPresetTier",
        back_populates="preset_obj"
    )

    categories = relationship(
        "Category",
        secondary=category_for_preset,
        back_populates="presets_using_it"
    )