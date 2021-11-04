from cmath import rect, phase
from math import sqrt, acos

from .base.base_business import BaseBusiness


class MotorBusiness(BaseBusiness):
    def treat_params(self, settings):
        settings['load'] = settings['load'] * 0.746
        settings['Il'] = self.__calculate_line_current(settings=settings)
        polar_params = self.__calculate_polar_params(settings)
        rect_params = self.__calculate_rectangular_params(settings=settings, polar_params=polar_params)
        return {
            'settings': settings,
            'polar': polar_params,
            'rect': rect_params,
        }

    def __calculate_polar_params(self, params: dict):
        polar_params = {'Vt': (params['Vt'], 0), 'Ia': self.__calculate_armor_current(params=params)}
        polar_params['Ea'] = self.__calculate_armor_voltage(params=params, polar_params=polar_params)
        polar_params['jXsIa'] = self.__calculate_reactive_power(params=params, polar_params=polar_params)
        return polar_params

    def __calculate_rectangular_params(self, settings: dict, polar_params: dict):
        return {
            'Vt': complex(settings['Vt'], 0),
            'Ia': rect(polar_params['Ia'][0], self.rad(polar_params['Ia'][1])),
            'Ea': rect(polar_params['Ea'][0], self.rad(polar_params['Ea'][1])),
            'jXsIa': rect(
                polar_params['jXsIa'][0], self.rad(polar_params['jXsIa'][1])
            ),
        }

    def __calculate_line_current(self, settings: dict):
        Pin = settings['load'] + settings['losses']
        return Pin * 1000 / (sqrt(3) * settings['Vt'] * settings['Fp'])

    def __calculate_armor_current(self, params: dict):
        current_module = params['Il'] / sqrt(3)
        current_phase = self.degree(acos(params['Fp']))
        if params['lagging']:
            current_phase *= -1
        return (current_module, current_phase)

    def __calculate_armor_voltage(self, params: dict, polar_params: dict):
        Vt = rect(params['Vt'], self.rad(0))
        jXs = rect(params['Xs'], self.rad(90))
        Ia = rect(polar_params['Ia'][0], self.rad(polar_params['Ia'][1]))
        Ea = Vt - jXs * Ia

        voltage_module = abs(Ea)
        voltage_phase = self.degree(phase(Ea))
        return (voltage_module, voltage_phase)

    def __calculate_reactive_power(self, params: dict, polar_params: dict):
        jXs = rect(params['Xs'], self.rad(90))
        Ia = rect(polar_params['Ia'][0], self.rad(polar_params['Ia'][1]))
        jXsIa = jXs * Ia

        reactive_power_module = abs(jXsIa)
        reactive_power_phase = self.degree(phase(jXsIa))
        return (reactive_power_module, reactive_power_phase)
