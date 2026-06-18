
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property

from scribesummer.src.ssum.model.interval_enum import IntervalEnum
from scribesummer.src.ssum.model.models.base_subscription import Subscription

class PresetBasedSubscription(Subscription):
    '''One of the user's paid subscriptions.
    Its attributes are specified by a preset for a particular
    company and subscription tier.

    This isn't a table in the database, its parent Subscription is.
    This class just specifies how the preset relationship works.
    
    QLAlchemy calls this "Single Table Inheritance".
    See: https://docs.sqlalchemy.org/en/20/orm/inheritance.html'''

    # Optional relationship to the preset it was defined with.
    preset_id: Mapped[str] = mapped_column(ForeignKey("subscription_preset.id"), nullable=True)

    # This Relationship object allows the preset to be easily retrieved in Python.
    preset_obj: Mapped["SubscriptionPreset"] = relationship( # type: ignore
        "SubscriptionPreset", uselist=False,
        back_populates="used_by"
    )

    # Also related to one of `SubscriptionPreset.tiers`.
    tier_id: Mapped[str] = mapped_column(ForeignKey("subscription_preset_tier.id"), nullable=True)
    tier_obj: Mapped["SubscriptionPresetTier"] = relationship( # type: ignore
        "SubscriptionPresetTier", uselist=False,
        back_populates="used_by"
    )

    @hybrid_property
    def name(self) -> str:
        '''Name of the subscription as determined by its preset.'''
        return self.tier_obj.name
    
    @hybrid_property
    def price_in_pence(self) -> int:
        '''Price in pence of this subscription as determined by its preset.'''
        return self.tier_obj.price_in_pence

    @hybrid_property
    def interval(self) -> IntervalEnum:
        '''Billing interval of this subscription as determined by its preset.'''
        return self.tier_obj.interval
    
    # Its `type` attribute will be set to "preset_based".
    __mapper_args__ = {
        "polymorphic_identity": "preset_based"
    }