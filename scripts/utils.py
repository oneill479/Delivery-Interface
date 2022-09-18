# Utilities for program
import enum
from datetime import timedelta


# enums to show package status
class Status(enum.Enum):
    AT_HUB = 1
    EN_ROUTE = 2
    DELIVERED = 3


# colors for print-outs
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = Blue = '\033[94m'
    GREY = '\033[90m'
    DEFAULT = '\033[0m'


# time class to add various times for deliveries
class Time:
    def __init__(self, hrs, mins):
        self.time = timedelta(
            hours=hrs,
            minutes=mins
        )

    # get the time
    def get_time(self):
        return self.time

    # add time
    def add_time(self, t_min):
        self.time = self.time + timedelta(
            minutes=t_min
        )
        return True

    # set start time
    def set_start_time(self, time):
        self.time = time
