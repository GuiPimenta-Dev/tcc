from cmath import rect, phase, rect, polar
from math import sqrt, acos

from business.base.base import BaseBusiness


class MotorBaseBusiness(BaseBusiness):
    def calculate_ia(self, settings: dict):
        current_module = settings['Il'] / sqrt(3)
        current_phase = self.degree(acos(settings['Fp']))
        if settings['lagging']:
            current_phase *= -1
        return (current_module, current_phase)

    def update_ia(self, settings: dict, rect_params: dict):
        Ia = polar((rect_params['Vt'] - rect_params['Ea']) / settings['Z'])

        return (Ia[0], self.degree(Ia[1]))

    def calculate_ea(self, settings: dict, polar_params: dict):
        Vt = rect(settings['Vt'], self.rad(0))
        Ia = rect(polar_params['Ia'][0], self.rad(polar_params['Ia'][1]))
        Ea = Vt - settings['Z'] * Ia

        voltage_module = abs(Ea)
        voltage_phase = self.degree(phase(Ea))
        return (voltage_module, voltage_phase)

    def calculate_jxsia(self, settings: dict, polar_params: dict):
        Ia = rect(polar_params['Ia'][0], self.rad(polar_params['Ia'][1]))
        jXsIa = settings['Z'] * Ia

        return (abs(jXsIa), self.degree(phase(jXsIa)))
