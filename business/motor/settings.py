from math import sqrt

from business.base.motor import MotorBaseBusiness
from models.motor import MotorModel


class Settings(MotorBaseBusiness):
    def create_motor(self, model: MotorModel):
        settings = self.__calculate_setings(model=model)

        polar_params = self.__polar_params(settings)
        rect_params = self.rectangular_params(polar_params=polar_params)
        return {
            'settings': settings,
            'polar': polar_params,
            'rect': rect_params,
        }

    def __calculate_setings(self, model: MotorModel):
        model = self.calculate_impedance(model=model)
        model['Il'] = self.__calculate_il(model=model)
        model['Ia'], model['theta'] = self.calculate_ia(model=model)
        model['Ea'], model['delta'] = self.calculate_ea(model=model)
        return model

    def __polar_params(self, settings: dict):
        return {
            'Vt': (settings['Vt'], 0),
            'Ia': (settings['Ia'], settings['theta']),
            'Ea': (settings['Ea'], settings['delta']),
            'RaIa': self.calculate_raia(settings=settings),
            'jXsIa': self.calculate_jxsia(settings=settings),
        }

    @staticmethod
    def __calculate_il(settings: dict):
        return settings['load'] * 1000 / (sqrt(3) * settings['Vt'] * settings['Fp'])
