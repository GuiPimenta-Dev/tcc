from math import sqrt, cos, sin

from business.base.generator.generator import GeneratorBaseBusiness


class IsolatedGeneratorBaseBusiness(GeneratorBaseBusiness):

    def calculate_settings(self, settings: dict):
        settings['Ia'], settings['theta'] = self.calculate_ia(settings=settings)
        settings = self.calculate_impedance(settings=settings)
        return settings

    def calculate_vt_module(self, settings: dict, polar_params: dict):
        equalty = polar_params['Ea'][0] ** 2 - (
                abs(settings['Xs']) * polar_params['Ia'][0] * cos(-1 * self.rad(polar_params['Ia'][1]))) ** 2
        Vt = sqrt(equalty) - (abs(settings['Xs']) * polar_params['Ia'][0] * sin(-1 * self.rad(polar_params['Ia'][1])))
        if not settings['delta']:
            Vt = sqrt(3) * Vt
        return (Vt, 0)


