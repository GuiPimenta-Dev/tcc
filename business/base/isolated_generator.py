from math import sqrt, cos, sin

from business.base.base import BaseBusiness


class IsolatedGeneratorBaseBusiness(BaseBusiness):
    def calculate_vt_module(self, settings: dict, polar_params: dict):
        equalty = polar_params['Ea'][0] ** 2 - (
                abs(settings['Xs']) * polar_params['Ia'][0] * cos(-1 * self.rad(polar_params['Ia'][1]))) ** 2
        Vt = sqrt(equalty) - (abs(settings['Xs']) * polar_params['Ia'][0] * sin(-1 * self.rad(polar_params['Ia'][1])))
        if not settings['delta']:
            Vt = sqrt(3) * Vt
        return (Vt, 0)

