from math import sqrt

from business.base.motor import MotorBaseBusiness


class Settings(MotorBaseBusiness):
    def create_motor(self, settings: dict):
        settings = self.__calculate_setings(settings=settings)

        polar_params = self.__polar_params(settings)
        rect_params = self.rectangular_params(polar_params=polar_params)
        return {
            'settings': settings,
            'polar': polar_params,
            'rect': rect_params,
        }

    def __calculate_setings(self, settings: dict):
        settings['kw_load'] = settings['load']
        settings['load'] = settings['load'] * 0.746 + settings['losses']
        settings = self.calculate_impedance(settings=settings)
        settings['Il'] = self.__calculate_il(settings=settings)
        settings['Ia'], settings['Ia_angle'] = self.calculate_ia(settings=settings)
        settings['Ea'], settings['Ea_angle'] = self.calculate_ea(settings=settings)
        return settings

    def __polar_params(self, settings: dict):
        return {
            'Vt': (settings['Vt'], 0),
            'Ia': (settings['Ia'], settings['Ia_angle']),
            'Ea': (settings['Ea'], settings['Ea_angle']),
            'RaIa': self.calculate_raia(settings=settings),
            'jXsIa': self.calculate_jxsia(settings=settings),
        }

    @staticmethod
    def __calculate_il(settings: dict):
        return settings['load'] * 1000 / (sqrt(3) * settings['Vt'] * settings['Fp'])
