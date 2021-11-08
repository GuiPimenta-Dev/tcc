from math import sin, asin

from business.base.isolated_generator import IsolatedGeneratorBaseBusiness


class Voltage(IsolatedGeneratorBaseBusiness):
    def voltage_update(self, params: dict, settings_voltage: tuple, voltage: float):
        settings, polar_params, _ = params.values()
        phase = self.__calculate_ea_phase(settings_voltage=settings_voltage, voltage=voltage)

        polar_params['Ea'] = (voltage, phase)
        polar_params['Ia'] = self._update_ia(settings=settings, polar_params=polar_params)
        polar_params['jXsIa'] = self.calculate_jxsia(settings=settings, polar_params=polar_params)

        params = {
            'polar': polar_params,
            'rect': self.rectangular_params(polar_params=polar_params)
        }
        return self.get_coords(params=params)

    def __calculate_ea_phase(self, settings_voltage: tuple, voltage: float):
        return self.degree(asin((settings_voltage[0] / voltage) * sin(self.rad(settings_voltage[1]))))
