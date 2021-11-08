from .motor.load import Load
from .motor.power_factor import PowerFactor
from .motor.settings import Settings
from .motor.voltage import Voltage


class Motor(Settings, Load, Voltage, PowerFactor):
    pass
