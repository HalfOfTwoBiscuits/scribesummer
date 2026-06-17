from typing import List

from sqlalchemy.orm import mapped_column, Mapped, relationship

from scribesummer.src.ssum.model.db import db
from scribesummer.src.ssum.model.models.timestamp_mixin import TimestampMixin

class User(db.Model, TimestampMixin):
    '''A user of the app. Has a budget.'''

    id: Mapped[int] = mapped_column(primary_key=True)
    budget_per_month: Mapped[int]

    subscriptions: Mapped[List["Subscription"]] = relationship( # type: ignore
        "Subscription",
        back_populates="user_obj"
    )