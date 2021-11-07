from .generator.load import Load
from .generator.power_factor import PowerFactor
from .generator.settings import Settings
from .generator.voltage import Voltage


class GeneratorBusiness(Settings, Load, Voltage, PowerFactor):
    pass
