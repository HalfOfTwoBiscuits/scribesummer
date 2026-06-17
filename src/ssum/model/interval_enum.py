from enum import Enum

class IntervalEnum(Enum):
    '''Enum for the billing interval of a subscription.'''
    
    WEEK = "w"
    MONTH = "m"
    YEAR = "y"