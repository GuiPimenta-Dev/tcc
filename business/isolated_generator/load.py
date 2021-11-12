from cmath import rect, phase
from math import asin

from business.base.generator.isolated_generator import IsolatedGeneratorBaseBusiness


class Load(IsolatedGeneratorBaseBusiness):

    def load_update(self, params: dict):
        settings, polar_params, _ = params.values()

        polar_params['Ia'] = (settings['Ia'], settings['theta'])
        polar_params['RaIa'] = self.calculate_raia(settings=settings)
        polar_params['jXsIa'] = self.calculate_jxsia(settings=settings)
        polar_params['Ea'] = (settings['Ea'], self.__calculate_ea_phase(settings=settings))
        polar_params['Vt'] = self.__calculate_vt(settings=settings, polar_params=polar_params)

        params = {
            'polar': polar_params,
            'rect': self.rectangular_params(polar_params=polar_params)
        }
        return self.get_coords(params=params)

    def __calculate_ea_phase(self, settings: dict):
        return self.degree(asin((abs(settings['Xs']) * settings['Ia'] * settings['Fp']) / settings['Ea']))

    def __calculate_vt(self, settings: dict, polar_params: dict):
        Ea = rect(polar_params['Ea'][0], self.rad(polar_params['Ea'][1]))
        Ia = rect(polar_params['Ia'][0], self.rad(polar_params['Ia'][1]))
        Vt = Ea - settings['Ra'] * Ia - settings['Xs'] * Ia

        voltage_module = abs(Vt)
        voltage_phase = self.degree(phase(Vt))
        return (voltage_module, voltage_phase)
