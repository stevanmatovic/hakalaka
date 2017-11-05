from enum import Enum
from hackathon.utils.utils import DataMessage
from hackathon.solution import test as c


class SolarState(Enum):
    BEFORE = 0
    DURING = 1
    AFTER = 2

def calc_solar_state(msg: DataMessage):
    hours = msg.id % 1440
    if hours < 7*60:
        c.solar_state = SolarState.BEFORE
    elif hours < 19*60:
        c.solar_state = SolarState.AFTER
    else:
        c.solar_state = SolarState.DURING