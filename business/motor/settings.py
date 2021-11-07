from math import sqrt

from business.base.motor import MotorBaseBusiness


class Settings(MotorBaseBusiness):
    def create_motor(self, settings):
        settings['load'] = settings['load'] * 0.746 + settings['losses']
        settings['Z'] = complex(settings['Ra'], settings['Xs'])
        settings['Il'] = self.__calculate_il(settings=settings)
        polar_params = self.__polar_params(settings)
        rect_params = self.rectangular_params(settings=settings, polar_params=polar_params)
        return {
            'settings': settings,
            'polar': polar_params,
            'rect': rect_params,
        }

    def __calculate_il(self, settings: dict):
        Pin = settings['load']
        return Pin * 1000 / (sqrt(3) * settings['Vt'] * settings['Fp'])

    def __polar_params(self, settings: dict):
        polar_params = {'Vt': (settings['Vt'], 0), 'Ia': self.calculate_ia(settings=settings)}
        polar_params['Ea'] = self.calculate_ea(settings=settings, polar_params=polar_params)
        polar_params['jXsIa'] = self.calculate_jxsia(settings=settings, polar_params=polar_params)
        return polar_params
