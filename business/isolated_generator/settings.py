from math import asin

from business.base.isolated_generator import IsolatedGeneratorBaseBusiness


class Settings(IsolatedGeneratorBaseBusiness):
    def create_generator(self, settings: dict):
        settings['Ia'] = self.calculate_ia_module(settings=settings)
        settings = self.calculate_impedance(settings=settings)
        polar_params = self.__isolated_polar_params(settings)
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
        polar_params['Ea'] = self.__calculate_ea_phase(settings=settings)
        polar_params['Vt'] = self.calculate_vt_module(settings=settings, polar_params=polar_params)

        return polar_params

    def __calculate_ea_phase(self, settings):
        phase = self.degree(asin((abs(settings['Z']) / settings['Ea']) * settings['Fp']))
        return (settings['Ea'], phase)
