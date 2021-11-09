from math import sin, asin

from business.base.connected_generator import ConnectedGeneratorBaseBusiness


class Voltage(ConnectedGeneratorBaseBusiness):
    def voltage_update(self, params: dict, settings_voltage: tuple, voltage: float):
        pass

