from sqlalchemy import Integer, String, ForeignKey, Enum
from sqlalchemy.orm import mapped_column, Mapped, relationship

from ssum.model.db import db
from ssum.model.duration_enum import DurationEnum
from ssum.model.models.timestamp_mixin import TimestampMixin

class SubscriptionPreset(db.Model, TimestampMixin):
    '''A pre-populated preset for a subscription of a certain brand.'''

    id = mapped_column(Integer(), primary_key=True)
    name = mapped_column(String(length=255), nullable=False)

    # Available tiers for this preset.
    tiers = relationship(
        "SubscriptionPresetTier",
        back_populates="preset_obj"
    )
