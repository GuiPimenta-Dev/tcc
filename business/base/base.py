from cmath import rect, phase
from math import sqrt, acos
from math import pi


class BaseBusiness:

    def get_coords(self, params: dict):
        return {
            'coords': self.__get_coords(params=params['rect']),
            'labels': self.__get_labels(params=params['polar']),
        }

    def rectangular_params(self, settings: dict, polar_params: dict):
        return {
            'Vt': complex(settings['Vt'], 0),
            'Ia': rect(polar_params['Ia'][0], self.rad(polar_params['Ia'][1])),
            'Ea': rect(polar_params['Ea'][0], self.rad(polar_params['Ea'][1])),
            'RaIa': rect(polar_params['RaIa'][0], self.rad(polar_params['RaIa'][1])),
            'jXsIa': rect(
                polar_params['jXsIa'][0], self.rad(polar_params['jXsIa'][1])
            ),
        }

    def __get_coords(self, params: dict):
        return {
            'Vt': (self.round(params['Vt'].real), self.round(params['Vt'].imag)),
            'Ia': (self.round(params['Ia'].real), self.round(params['Ia'].imag)),
            'Ea': (self.round(params['Ea'].real), self.round(params['Ea'].imag)),
            'RaIa': (self.round(params['RaIa'].real), self.round(params['RaIa'].imag)),
            'jXsIa': (self.round(params['jXsIa'].real), self.round(params['jXsIa'].imag)),
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
        current_module = settings['Il']
        if settings['delta']:
            current_module = current_module / sqrt(3)

        current_phase = self.degree(acos(settings['Fp']))
        if settings['lagging']:
            current_phase *= -1
        return (current_module, current_phase)

    def calculate_raia(self, settings: dict, polar_params: dict):
        Ia = rect(polar_params['Ia'][0], self.rad(polar_params['Ia'][1]))
        Ra = settings['Ra'] * Ia

        return (abs(Ra), self.degree(phase(Ra)))

    def calculate_jxsia(self, settings: dict, polar_params: dict):
        Ia = rect(polar_params['Ia'][0], self.rad(polar_params['Ia'][1]))
        jXsIa = settings['Xs'] * Ia

        return (abs(jXsIa), self.degree(phase(jXsIa)))

    def calculate_impedance(self, settings: dict):
        settings['Xs'] = complex(0, settings['Xs'])
        settings['Ra'] = complex(settings['Ra'], 0)
        settings['Z'] = settings['Ra'] + settings['Xs']
        return settings

    @staticmethod
    def round(x: float):
        return round(x, 2)

    @staticmethod
    def degree(x: float):
        return (x * 180) / pi

    @staticmethod
    def rad(x: float):
        return (x * pi) / 180
