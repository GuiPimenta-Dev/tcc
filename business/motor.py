from cmath import rect, phase, polar
from math import sqrt, acos, asin

from .base.base import BaseBusiness


class MotorBusiness(BaseBusiness):
    def treat_params(self, settings):
        settings['load'] = settings['load'] * 0.746 + settings['losses']
        settings['Z'] = settings['Xs'] + settings['Ra']
        settings['Il'] = self.__calculate_line_current(settings=settings)
        polar_params = self.__calculate_polar_params(settings)
        rect_params = self.__calculate_rectangular_params(settings=settings, polar_params=polar_params)
        return {
            'settings': settings,
            'polar': polar_params,
            'rect': rect_params,
        }

    def __calculate_polar_params(self, settings: dict):
        polar_params = {'Vt': (settings['Vt'], 0), 'Ia': self.__calculate_armor_current(settings=settings)}
        polar_params['Ea'] = self._calculate_armor_voltage(settings=settings, polar_params=polar_params)
        polar_params['jXsIa'] = self.__calculate_reactive_power(settings=settings, polar_params=polar_params)
        return polar_params

    def __calculate_rectangular_params(self, settings: dict, polar_params: dict):
        return {
            'Vt': complex(settings['Vt'], 0),
            'Ia': rect(polar_params['Ia'][0], self.rad(polar_params['Ia'][1])),
            'Ea': rect(polar_params['Ea'][0], self.rad(polar_params['Ea'][1])),
            'jXsIa': rect(
                polar_params['jXsIa'][0], self.rad(polar_params['jXsIa'][1])
            ),
        }

    def __calculate_line_current(self, settings: dict):
        Pin = settings['load']
        return Pin * 1000 / (sqrt(3) * settings['Vt'] * settings['Fp'])

    def __calculate_armor_current(self, settings: dict):
        current_module = settings['Il'] / sqrt(3)
        current_phase = self.degree(acos(settings['Fp']))
        if settings['lagging']:
            current_phase *= -1
        return (current_module, current_phase)

    def _calculate_armor_voltage(self, settings: dict, polar_params: dict):
        Vt = rect(settings['Vt'], self.rad(0))
        jXs = rect(settings['Z'], self.rad(90))
        Ia = rect(polar_params['Ia'][0], self.rad(polar_params['Ia'][1]))
        Ea = Vt - jXs * Ia

        voltage_module = abs(Ea)
        voltage_phase = self.degree(phase(Ea))
        return (voltage_module, voltage_phase)

    def __calculate_reactive_power(self, settings: dict, polar_params: dict):
        jXs = rect(settings['Xs'], self.rad(90))
        Ia = rect(polar_params['Ia'][0], self.rad(polar_params['Ia'][1]))
        jXsIa = jXs * Ia

        reactive_power_module = abs(jXsIa)
        reactive_power_phase = self.degree(phase(jXsIa))
        return (reactive_power_module, reactive_power_phase)

    def ea_phase_from_load_update(self, params: dict):
        settings, polar_params, rect_params = params.values()
        phase = (settings['load'] * settings['Z'] * 1000) / (3 * settings['Vt'] * polar_params['Ea'][0])

        if phase > 1:
            y = int(phase)
            phase = phase - y

        phase = self.rad(-1 * self.degree(asin(phase)))

        Ea = (params['polar']['Ea'][0], phase)

        Ia = self.__ia_from_load_update(params=params, Ea=Ea)

        jXsIa = self.__jxsia_from_load_update(params=params, Ia=Ia)

        params = {
            'polar': {'Vt': polar_params['Vt'], 'Ea': (Ea[0], self.degree(Ea[1])), 'Ia': Ia, 'jXsIa': jXsIa},
            'rect': {
                'Vt': rect_params['Vt'],
                'Ea': rect(Ea[0], self.rad(Ea[1])),
                'Ia': rect(Ia[0], self.rad(Ia[1])),
                'jXsIa': rect(jXsIa[0], self.rad(jXsIa[1])),
            }
        }
        return self.get_coords(params=params)

    def __ia_from_load_update(self, params: dict, Ea):

        # polar_params['Vt'] = polar_params['Vt'] + 0j

        # Ea = rect(Ea[0], self.rad(Ea[1]))
        settings, polar_params, rect_params = params.values()
        numerador = polar(rect_params['Vt'] - rect(Ea[0], Ea[1]))
        denominador = polar(complex(0, settings['Z']))

        return (numerador[0] / denominador[0], self.degree(numerador[1] - denominador[1]))

    def __jxsia_from_load_update(self, params: dict, Ia):
        settings, _, _ = params.values()
        jXs = rect(settings['Z'], self.rad(90))
        Ia = rect(Ia[0], self.rad(Ia[1]))
        jXsIa = jXs * Ia
        return (abs(jXsIa), self.degree(phase(jXsIa)))
