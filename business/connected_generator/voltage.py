from business.base.generator import GeneratorBaseBusiness
from math import asin
from cmath import rect, phase
from copy import deepcopy


class Voltage(GeneratorBaseBusiness):
    def voltage_update(self, settings: dict):
        delta = self.__calculate_new_delta(settings=settings)
        Ia = self.__calculate_new_ia(settings=settings, delta=delta)
        polar_params = self.__polar_params(settings=settings, Ia=Ia, delta=delta)

        params = {
            'polar': polar_params,
            'rect': self.rectangular_params(polar_params=polar_params)
        }
        return self.get_coords(params=params)

    def __calculate_new_delta(self, settings: dict):
        return self.degree(asin((settings['Ia'] * settings['Fp'] * abs(settings['Xs'])) / settings['Ea']))

    def __calculate_new_ia(self, settings: dict, delta: float):
        Vt = rect(settings['Vt'], 0)
        Ea = rect(settings['Ea'], self.rad(delta))
        Ia = (Ea - Vt) / settings['Z']

        current_module = abs(Ia)
        current_phase = self.degree(phase(Ia))
        return (current_module, current_phase)

    def __polar_params(self, settings: dict, Ia: tuple, delta: float):
        new_settings = deepcopy(settings)
        new_settings['Ia'], new_settings['theta'] = Ia[0], Ia[1]
        return {
            'Vt': (settings['Vt'], 0),
            'Ia': Ia,
            'RaIa': self.calculate_raia(settings=new_settings),
            'jXsIa': self.calculate_jxsia(settings=new_settings),
            'Ea': (settings['Ea'], delta),
        }
