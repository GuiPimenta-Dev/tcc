from cmath import rect, phase
from math import sqrt, cos, sin

from business.base.base import BaseBusiness


class GeneratorBaseBusiness(BaseBusiness):
    def calculate_settings(self, settings: dict):
        settings = self.calculate_impedance(settings=settings)
        settings['Ia'], settings['Ia_angle'] = self.calculate_ia(settings=settings)
        settings['Ea'], settings['Ea_angle'] = self.calculate_ea(settings=settings)
        return settings

    def calculate_ea(self, settings: dict):
        Vt = rect(settings['Vt'], 0)
        Ia = rect(settings['Ia'], self.rad(settings['Ia_angle']))
        Ea = Vt + settings['Ra'] * Ia + settings['Xs'] * Ia

        voltage_module = abs(Ea)
        voltage_phase = self.degree(phase(Ea))
        return (voltage_module, voltage_phase)

    def power_factor_update(self, params: dict):
        settings, polar_params, rect_params = params.values()
        settings['Ia'], settings['Ia_angle'] = self.calculate_ia(settings=settings)

        polar_params['Ia'] = (settings['Ia'], settings['Ia_angle'])
        polar_params['RaIa'] = self.calculate_raia(settings=settings)
        polar_params['jXsIa'] = self.calculate_jxsia(settings=settings)
        polar_params['Ea'] = self.calculate_ea(settings=settings)

        params = {
            'polar': polar_params,
            'rect': self.rectangular_params(polar_params=polar_params)
        }
        return self.get_coords(params=params)



