from cmath import rect, phase
from copy import deepcopy
from math import sin, sqrt, cos

from business.base.generator import GeneratorBaseBusiness


class Voltage(GeneratorBaseBusiness):
    def voltage_update(self, params: dict):
        settings, polar_params, _ = params.values()
        delta = self.calculate_new_delta(settings=settings)
        Ia_cos_theta = rect(settings['Ia'], settings['Fp'])
        Ia_sin_theta = self.__calculate_ia_sin_theta(settings=settings, delta=delta)
        Ia = self.__calculate_ia(Ia_sin_theta=Ia_sin_theta, Ia_cos_theta=Ia_cos_theta)
        Vt = self.__calculate_vt(settings=settings, Ia_sin_theta=Ia_sin_theta, Ia_cos_theta=Ia_cos_theta, delta=delta)
        polar_params = self.__polar_params(settings=settings, Vt=Vt, Ia=Ia, delta=delta)

        params = {
            'polar': polar_params,
            'rect': self.rectangular_params(polar_params=polar_params)
        }

        return self.get_coords(params=params)

    def __calculate_ia_sin_theta(self, settings: dict, delta: float):
        Ea_sin_theta = rect(settings['Ea'], sin(self.rad(delta)))
        XsIa_cos_theta = settings['Xs'] * settings['Fp'] * settings['Ia']
        # TODO E se Ra for 0 ?
        Ia_sin_theta = (Ea_sin_theta - XsIa_cos_theta) / settings['Ra']
        return Ia_sin_theta

    def __calculate_ia(self, Ia_sin_theta, Ia_cos_theta):
        module_ia = sqrt(abs(Ia_cos_theta) ** 2 + abs(Ia_sin_theta) ** 2)
        phase_ia = self.degree(phase(Ia_cos_theta) ** 2 + phase(Ia_sin_theta) ** 2)
        return (module_ia, phase_ia)

    def __calculate_vt(self, settings, Ia_sin_theta, Ia_cos_theta, delta):
        Ea_cos_delta = rect(settings['Ea'], cos(self.rad(delta)))
        Vt = Ea_cos_delta - (settings['Ra'] * Ia_cos_theta) - (settings['Xs'] * Ia_sin_theta)
        voltage_module = abs(Vt)
        voltage_phase = self.degree(phase(Vt))
        return (voltage_module, voltage_phase)

    def __polar_params(self, settings: dict, Ia: tuple, Vt: tuple, delta):
        new_settings = deepcopy(settings)
        new_settings['Ia'], new_settings['Ia_angle'] = Ia[0], Ia[1]
        return {
            'Vt': Vt,
            'Ia': Ia,
            'RaIa': self.calculate_raia(settings=new_settings),
            'jXsIa': self.calculate_jxsia(settings=new_settings),
            'Ea': (settings['Ea'], delta),
        }
