from typing import List

from sqlalchemy.orm import mapped_column, Mapped, relationship

from scribesummer.src.ssum.model.db import db
from scribesummer.src.ssum.model.models.timestamp_mixin import TimestampMixin

class Category(db.Model, TimestampMixin):
    '''A pre-populated category of subscription that can be used as a filter.
    Also determines the displayed icon for a preset.
    The icon's filename is its ID.'''

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]

    custom_subscriptions_using_it: Mapped[List["CustomSubscription"]] = relationship( # type: ignore
        "CustomSubscription",
        secondary="category_for_custom_sub",
        back_populates="categories"
    )

    presets_using_it: Mapped[List["SubscriptionPreset"]] = relationship( # type: ignore
        "SubscriptionPreset",
        secondary="category_for_preset",
        back_populates="categories"
    )