from cmath import rect, phase
from math import pi, sqrt, acos


class BaseBusiness:

    def get_coords(self, params: dict):
        return {
            'coords': self.__get_coords(params=params['rect']),
            'labels': self.__get_labels(params=params['polar']),
        }

    def rectangular_params(self, polar_params: dict):
        return {
            'Vt': rect(polar_params['Vt'][0], self.rad(polar_params['Vt'][1])),
            'Ia': rect(polar_params['Ia'][0], self.rad(polar_params['Ia'][1])),
            'Ea': rect(polar_params['Ea'][0], self.rad(polar_params['Ea'][1])),
            'RaIa': rect(polar_params['RaIa'][0], self.rad(polar_params['RaIa'][1])),
            'jXsIa': rect(
                polar_params['jXsIa'][0], self.rad(polar_params['jXsIa'][1])
            ),
        }

    def __get_coords(self, params: dict):
        max_coord = 0
        for value in params.values():
            if abs(value.real) > max_coord:
                max_coord = abs(value.real)

            if abs(value.imag) > max_coord:
                max_coord = abs(value.imag)

        coef = 45 / max_coord

        return {
            'Vt': (self.round(params['Vt'].real * coef), self.round(params['Vt'].imag) * coef),
            'Ia': (self.round(params['Ia'].real * coef), self.round(params['Ia'].imag) * coef),
            'Ea': (self.round(params['Ea'].real * coef), self.round(params['Ea'].imag) * coef),
            'RaIa': (self.round(params['RaIa'].real * coef), self.round(params['RaIa'].imag) * coef),
            'jXsIa': (self.round(params['jXsIa'].real * coef), self.round(params['jXsIa'].imag) * coef),
        }

    def __get_labels(self, params: dict):
        return {
            'Vt': f'{self.round(params["Vt"][0])} ∠ {self.round(params["Vt"][1])}°',
            'Ia': f'{self.round(params["Ia"][0])} ∠ {self.round(params["Ia"][1])}°',
            'Ea': f'{self.round(params["Ea"][0])} ∠ {self.round(params["Ea"][1])}°',
            'RaIa': f'{self.round(params["RaIa"][0])} ∠ {self.round(params["RaIa"][1])}°',
            'jXsIa': f'{self.round(params["jXsIa"][0])} ∠ {self.round(params["jXsIa"][1])}°'
        }

    def calculate_ia(self, settings: dict):
        module = settings['Il']
        if settings['delta']:
            module = module / sqrt(3)

        phase = self.degree(acos(settings['Fp']))
        if settings['lagging'] and phase != 0.0:
            phase *= -1

        return (module, phase)

    def calculate_raia(self, settings: dict):
        Ia = rect(settings['Ia'], self.rad(settings['Ia_angle']))
        Ra = settings['Ra'] * Ia

        return (abs(Ra), self.degree(phase(Ra)))

    def calculate_jxsia(self, settings: dict):
        Ia = rect(settings['Ia'], self.rad(settings['Ia_angle']))
        jXsIa = settings['Xs'] * Ia

        return (abs(jXsIa), self.degree(phase(jXsIa)))

    @staticmethod
    def calculate_impedance(settings: dict):
        settings['Xs'] = complex(0, settings['Xs'])
        settings['Ra'] = complex(settings['Ra'], 0)
        settings['Z'] = settings['Ra'] + settings['Xs']
        return settings

    @staticmethod
    def parse_revolutions(phase: float):
        return phase - int(phase)

    @staticmethod
    def round(x: float):
        return round(x, 2)

    @staticmethod
    def degree(x: float):
        return (x * 180) / pi

    @staticmethod
    def rad(x: float):
        return (x * pi) / 180
