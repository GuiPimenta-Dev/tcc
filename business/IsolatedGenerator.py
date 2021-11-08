from .isolated_generator.load import Load
from .isolated_generator.power_factor import PowerFactor
from .isolated_generator.settings import Settings
from .isolated_generator.voltage import Voltage


class IsolatedGenerator(Settings, Load, Voltage, PowerFactor):
    pass
