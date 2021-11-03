from abc import ABC, abstractmethod
from math import pi

class BaseBusiness(ABC):

    @staticmethod
    @abstractmethod
    def treat_params(params: dict):
        pass

    @staticmethod
    def round(x: float):
        return round(x, 2)

    @staticmethod
    def degree(x: float):
        return (x * 180) / pi

    @staticmethod
    def rad(x: float):
        return (x * pi) / 180

