from math import sin, asin

from business.base.isolated_generator import IsolatedGeneratorBaseBusiness


class Voltage(IsolatedGeneratorBaseBusiness):
    def voltage_update(self, params: dict, settings_voltage: tuple, voltage: float):
        settings, polar_params, _ = params.values()
        phase = self.__calculate_ea_phase(settings_voltage=settings_voltage, voltage=voltage)
        pass

    def __calculate_ea_phase(self, settings_voltage: tuple, voltage: float):
        return self.degree(asin((settings_voltage[0] / voltage) * sin(self.rad(settings_voltage[1]))))