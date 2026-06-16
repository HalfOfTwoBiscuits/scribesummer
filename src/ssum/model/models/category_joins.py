from sqlalchemy import Column, ForeignKey

from scribesummer.src.ssum.model.db import db

# Joining tables for the many-to-many relationships between
# custom subscriptions and categories, and subscription presets and categories.
# Specified using non-declarative syntax as suggested in the docs at:
# https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#setting-bi-directional-many-to-many
category_for_custom_sub = db.Table(
    "category_for_custom_sub",
    db.Model.metadata,
    Column("category_id", ForeignKey("Category.id"), primary_key=True),
    Column("subscription_id", ForeignKey("CustomSubscription.id"), primary_key=True)
)

category_for_preset = db.Table(
    "category_for_custom_sub",
    db.Model.metadata,
    Column("category_id", ForeignKey("Category.id"), primary_key=True),
    Column("subscription_id", ForeignKey("SubscriptionPreset.id"), primary_key=True)
)