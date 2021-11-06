from cmath import rect, phase, polar
from math import asin

from .base import MotorBaseBusiness


class Load(MotorBaseBusiness):

    def load_update(self, params: dict):
        settings, polar_params, rect_params = params.values()
        phase = (settings['load'] * settings['Z'] * 1000) / (3 * settings['Vt'] * polar_params['Ea'][0])

        if phase > 1:
            y = int(phase)
            phase = phase - y

        phase = self.rad(-1 * self.degree(asin(phase)))

        Ea = (params['polar']['Ea'][0], phase)

        polar_params['Ia'] = self.__updated_ia(params=params, Ea=Ea)
        polar_params['Ea'] = (Ea[0], self.degree(Ea[1]))
        polar_params['jXsIa'] = self.__updated_jxsia(params=params, Ia=polar_params['Ia'])

        params = {
            'polar': polar_params,
            'rect': self.rectangular_params(settings=settings, polar_params=polar_params)
        }
        return self.get_coords(params=params)

    def __updated_ia(self, params: dict, Ea):
        
        settings, polar_params, rect_params = params.values()
        numerator = polar(rect_params['Vt'] - rect(Ea[0], Ea[1]))
        denominator = polar(complex(0, settings['Z']))

        return (numerator[0] / denominator[0], self.degree(numerator[1] - denominator[1]))

    def __updated_jxsia(self, params: dict, Ia):
        settings, _, _ = params.values()
        jXs = rect(settings['Z'], self.rad(90))
        Ia = rect(Ia[0], self.rad(Ia[1]))
        jXsIa = jXs * Ia
        return (abs(jXsIa), self.degree(phase(jXsIa)))
