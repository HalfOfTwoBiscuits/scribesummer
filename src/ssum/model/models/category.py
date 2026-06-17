from typing import List

from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from scribesummer.src.ssum.model.db import db
from scribesummer.src.ssum.model.models.timestamp_mixin import TimestampMixin

class Category(db.Model, TimestampMixin):
    '''A pre-populated category of subscription that can be used as a filter.
    Also determines the displayed icon for a preset.
    The icon's filename is its ID.'''

    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    name: Mapped[str] = mapped_column(String(255))

    custom_subscriptions_using_it: Mapped[List["CustomSubscription"]] = relationship( # type: ignore
        "CustomSubscription",
        secondary="category_for_custom_sub",
        back_populates="categories"
    )

    tiers_using_it: Mapped[List["SubscriptionPresetTier"]] = relationship( # type: ignore
        "SubscriptionPresetTier",
        secondary="category_for_tier",
        back_populates="categories"
    )