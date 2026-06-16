from datetime import datetime, timezone

from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.sql import func

class TimestampMixin:
    '''A utility mixin that provides create and update timestamps.
    Used for all models via multiple inheritance.

    A mixin is necessary because the models need to inherit from db.Model,
    and if they had a base class which did that, then the base class would be a model too.'''

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        # Use a lambda to get the current UTC timestamp
        # on the Python end, when updating the record.
        onupdate=lambda: datetime.now(timezone.utc).replace(tzinfo=None)
    )