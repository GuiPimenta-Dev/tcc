from math import sqrt

from business.base.generator import GeneratorBaseBusiness


class Settings(GeneratorBaseBusiness):
    def create_generator(self, settings: dict):
        settings['Ia'] = self.__calculate_ia(settings=settings)
        settings = self.calculate_impedance(settings=settings)
        polar_params = self.__polar_params(settings)
        rect_params = self.rectangular_params(polar_params=polar_params)
        return {
            'settings': settings,
            'polar': polar_params,
            'rect': rect_params,
        }

    def __polar_params(self, settings: dict):
        polar_params = {'Ia': self.calculate_ia(settings=settings)}
        polar_params['RaIa'] = self.calculate_raia(settings=settings, polar_params=polar_params)
        polar_params['jXsIa'] = self.calculate_jxsia(settings=settings, polar_params=polar_params)
        polar_params['Vt'] = self.calculate_vt(settings=settings, polar_params=polar_params, Ea=settings['Ea'] )
        polar_params['Ea'] = self.calculate_ea(settings=settings, polar_params=polar_params)

        return polar_params

    @staticmethod
    def __calculate_ia(settings: dict):
        Ia = settings['Il']
        if settings['delta']:
            Ia = Ia / sqrt(3)

        return Ia
