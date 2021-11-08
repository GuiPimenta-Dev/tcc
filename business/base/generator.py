from cmath import phase, rect
from math import sqrt, acos, cos, sin

from business.base.base import BaseBusiness


class GeneratorBaseBusiness(BaseBusiness):

    def calculate_connected_ea(self, settings: dict, polar_params: dict):
        Vt = rect(polar_params['Vt'][0], self.rad(polar_params['Vt'][1]))
        Ia = rect(polar_params['Ia'][0], self.rad(polar_params['Ia'][1]))
        Ea = Vt + settings['Ra'] * Ia + settings['Xs'] * Ia

        voltage_module = abs(Ea)
        voltage_phase = self.degree(phase(Ea))
        return (voltage_module, voltage_phase)

    def calculate_isolated_vt_module(self, settings: dict, polar_params: dict):
        equalty = polar_params['Ea'][0] ** 2 - (
                abs(settings['Xs']) * polar_params['Ia'][0] * cos(-1 * self.rad(polar_params['Ia'][1]))) ** 2
        Vt = sqrt(equalty) - (abs(settings['Xs']) * polar_params['Ia'][0] * sin(-1 * self.rad(polar_params['Ia'][1])))
        if not settings['delta']:
            Vt = sqrt(3) * Vt
        return (Vt, 0)
