from cmath import rect, phase
from math import asin

from business.base.generator import GeneratorBaseBusiness


class Load(GeneratorBaseBusiness):

    def load_update(self, params: dict):
        settings, _, _ = params.values()

        polar_params = self.__polar_params(settings=settings)
        params = {
            'polar': polar_params,
            'rect': self.rectangular_params(polar_params=polar_params)
        }
        return self.get_coords(params=params)

    def __polar_params(self, settings: dict):
        polar_params = {'Ia': (settings['Ia'], settings['Ia_angle']), 'RaIa': self.calculate_raia(settings=settings),
                        'jXsIa': self.calculate_jxsia(settings=settings),
                        'Ea': (settings['Ea'], self.__calculate_ea_phase(settings=settings))}
        polar_params['Vt'] = self.__calculate_vt(settings=settings, polar_params=polar_params)
        return polar_params

    def __calculate_ea_phase(self, settings: dict):
        phase = (abs(settings['Xs']) * settings['Ia'] * settings['Fp']) / settings['Ea']
        phase = self.parse_revolutions(phase)

        return self.degree(asin(phase))

    def __calculate_vt(self, settings: dict, polar_params: dict):
        Ea = rect(polar_params['Ea'][0], self.rad(polar_params['Ea'][1]))
        Ia = rect(polar_params['Ia'][0], self.rad(polar_params['Ia'][1]))
        Vt = Ea - settings['Ra'] * Ia - settings['Xs'] * Ia

        voltage_module = abs(Vt)
        voltage_phase = self.degree(phase(Vt))
        return (voltage_module, voltage_phase)
