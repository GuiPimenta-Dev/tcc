from .motor.settings import Settings
from .motor.load import Load
from .motor.voltage import Voltage
from .motor.power_factor import PowerFactor


class MotorBusiness(Settings, Load, Voltage, PowerFactor):
    pass
