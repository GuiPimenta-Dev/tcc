from .motor.settings import Settings
from .motor.load import Load
from .motor.power_factor import PowerFactor

class MotorBusiness(Settings, Load, PowerFactor):
    pass