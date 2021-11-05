from abc import ABC, abstractmethod
from math import pi


class BaseBusiness(ABC):



    @abstractmethod
    def treat_params(self, params: dict):
        pass


    def get_coords(self, params: dict):
        return {
            'coords': self.__get_coords(params=params['rect']),
            'labels': self.__get_labels(params=params['polar']),
        }


    def __get_coords(self, params: dict):
        return {
            'Vt': (self.round(params['Vt'].real), self.round(params['Vt'].imag)),
            'Ia': (self.round(params['Ia'].real), self.round(params['Ia'].imag)),
            'Ea': (self.round(params['Ea'].real), self.round(params['Ea'].imag)),
            'jXsIa': (self.round(params['jXsIa'].real), self.round(params['jXsIa'].imag)),
        }


    def __get_labels(self,params: dict):
        return {
            'Vt': f'{self.round(params["Vt"][0])} ∠ {self.round(params["Vt"][1])}°',
            'Ia': f'{self.round(params["Ia"][0])} ∠ {self.round(params["Ia"][1])}°',
            'Ea': f'{self.round(params["Ea"][0])} ∠ {self.round(params["Ea"][1])}°',
            'jXsIa': f'{self.round(params["jXsIa"][0])} ∠ {self.round(params["jXsIa"][1])}°'
        }

    @staticmethod
    def round(x: float):
        return round(x, 2)

    @staticmethod
    def degree(x: float):
        return (x * 180) / pi

    @staticmethod
    def rad(x: float):
        return (x * pi) / 180

