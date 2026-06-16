from sqlalchemy import Column, ForeignKey

from scribesummer.src.ssum.model.db import db

from scribesummer.src.ssum.model.models.category import Category
from scribesummer.src.ssum.model.models.subscription_preset import SubscriptionPreset

# Joining table for the many-to-many relationship between
# presets and categories.
# Specified using non-declarative syntax as suggested in the docs at:
# https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#setting-bi-directional-many-to-many
category_for_preset = db.Table(
    "category_for_preset",
    db.Model.metadata,
    Column("category_id", ForeignKey(Category.id), primary_key=True),
    Column("subscription_id", ForeignKey(SubscriptionPreset.id), primary_key=True),
    extend_existing=True
)