from enum import Enum

class IntervalEnum(Enum):
    '''Enum for the billing interval of a subscription.'''
    
    WEEK = 1
    MONTH = 2
    YEAR = 3