from math import sqrt, asin, cos, sin

from business.base.generator import GeneratorBaseBusiness


class Settings(GeneratorBaseBusiness):
    def create_generator(self, settings: dict):
        settings['Ia'] = self.calculate_ia_module(settings=settings)
        settings = self.calculate_impedance(settings=settings)
        if settings['isolated']:
            polar_params = self.__isolated_polar_params(settings)
        else:
            polar_params = self.__connected_polar_params(settings)
        rect_params = self.rectangular_params(polar_params=polar_params)
        return {
            'settings': settings,
            'polar': polar_params,
            'rect': rect_params,
        }

    def __isolated_polar_params(self, settings: dict):
        polar_params = {'Ia': self.calculate_ia(settings=settings)}
        polar_params['RaIa'] = self.calculate_raia(settings=settings, polar_params=polar_params)
        polar_params['jXsIa'] = self.calculate_jxsia(settings=settings, polar_params=polar_params)
        polar_params['Ea'] = self.__calculate_isolated_ea_phase(settings=settings)
        polar_params['Vt'] = self.calculate_isolated_vt_module(settings=settings, polar_params=polar_params)

        return polar_params

    def __connected_polar_params(self, settings: dict):
        polar_params = {'Vt': (settings['Vt'], 0), 'Ia': self.calculate_ia(settings=settings)}
        polar_params['RaIa'] = self.calculate_raia(settings=settings, polar_params=polar_params)
        polar_params['jXsIa'] = self.calculate_jxsia(settings=settings, polar_params=polar_params)
        polar_params['Ea'] = self.calculate_connected_ea(settings=settings, polar_params=polar_params)

        return polar_params

    def __calculate_isolated_ea_phase(self, settings):
        phase = self.degree(asin((abs(settings['Z']) / settings['Ea']) * settings['Fp']))
        return (settings['Ea'], phase)

