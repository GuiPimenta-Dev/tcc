from .connected_generator.load import Load
from .connected_generator.power_factor import PowerFactor
from .connected_generator.settings import Settings
from .connected_generator.voltage import Voltage


class ConnectedGenerator(Settings, Load, Voltage, PowerFactor):
    pass
