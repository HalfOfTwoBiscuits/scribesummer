from enum import Enum
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

class DurationEnum(Enum):
    WEEK = 1
    MONTH = 2
    YEAR = 3

    def next_renewal(self) -> datetime:
        '''Return the next time this subscription needs renewing.'''

        now = datetime.now()

        # Use the relativedelta class to account for leap years
        # and differing amounts of days in a month.
        match (self):
            case DurationEnum.WEEK: return now + timedelta(weeks=1)
            case DurationEnum.MONTH: return now + relativedelta(months=1)
            case DurationEnum.YEAR: return now + relativedelta(years=1)