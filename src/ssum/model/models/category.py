from sqlalchemy import Integer
from sqlalchemy.orm import mapped_column, Mapped, relationship

from ssum.model.db import db
from ssum.model.models.timestamp_mixin import TimestampMixin
from ssum.model.models.category_joins import category_for_custom_sub, category_for_preset

class Category(db.Model, TimestampMixin):
    '''A category of subscription that can be used as a filter.
    Also determines the displayed icon for a preset.'''

    id = mapped_column(Integer(), primary_key=True)
    name = Mapped[str]

    custom_subscriptions_using_it = relationship(
        "CustomSubscription",
        secondary=category_for_custom_sub,
        back_populates="categories"
    )

    presets_using_it = relationship(
        "SubscriptionPreset",
        secondary=category_for_preset,
        back_populates="categories"
    )