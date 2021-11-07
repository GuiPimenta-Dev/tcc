from cmath import phase, rect, polar
from math import sqrt, cos, sin

from business.base.base import BaseBusiness


class GeneratorBaseBusiness(BaseBusiness):

    def update_ia(self, settings: dict, rect_params: dict):
        Ia = polar((rect_params['Vt'] - rect_params['Ea']) / settings['Z'])

        return (Ia[0], self.degree(Ia[1]))

    def calculate_vt(self, settings: dict, polar_params: dict, Ea: float):
        equalty = Ea ** 2 - (abs(settings['Xs']) * polar_params['Ia'][0] * cos(self.rad(polar_params['Ia'][1]))) ** 2
        Vt = sqrt(equalty) - (abs(settings['Xs']) * polar_params['Ia'][0] * sin(self.rad(polar_params['Ia'][1])))
        if not settings['delta']:
            Vt = sqrt(3) * Vt
        return (Vt, 0)

    def calculate_ea(self, settings: dict, polar_params: dict):
        Vt = rect(polar_params['Vt'][0], self.rad(polar_params['Vt'][1]))
        Ia = rect(polar_params['Ia'][0], self.rad(polar_params['Ia'][1]))
        Ea = Vt + settings['Ra'] * Ia + settings['Xs'] * Ia

        voltage_module = abs(Ea)
        voltage_phase = self.degree(phase(Ea))
        return (voltage_module, voltage_phase)
