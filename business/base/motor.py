from cmath import phase, rect, polar
from math import sqrt, acos

from business.base.base import BaseBusiness


class MotorBaseBusiness(BaseBusiness):

    def update_ia(self, settings: dict, rect_params: dict):
        Ia = polar((rect_params['Vt'] - rect_params['Ea']) / settings['Z'])

        return (Ia[0], self.degree(Ia[1]))

    def calculate_ea(self, settings: dict, polar_params: dict):
        Vt = rect(settings['Vt'], self.rad(0))
        Ia = rect(polar_params['Ia'][0], self.rad(polar_params['Ia'][1]))
        Ea = Vt - settings['Ra'] * Ia - settings['Xs'] * Ia

        voltage_module = abs(Ea)
        voltage_phase = self.degree(phase(Ea))
        return (voltage_module, voltage_phase)
