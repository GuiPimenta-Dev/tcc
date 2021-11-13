from business.base.generator import GeneratorBaseBusiness


class Settings(GeneratorBaseBusiness):
    def create_generator(self, settings: dict):
        settings = self.calculate_settings(settings=settings)
        polar_params = self.__polar_params(settings)
        rect_params = self.rectangular_params(polar_params=polar_params)
        return {
            'settings': settings,
            'polar': polar_params,
            'rect': rect_params,
        }

    def __polar_params(self, settings: dict):
        return {
            'Vt': (settings['Vt'], 0),
            'Ia': self.calculate_ia(settings=settings),
            'RaIa': self.calculate_raia(settings=settings),
            'jXsIa': self.calculate_jxsia(settings=settings),
            'Ea': self.calculate_ea(settings=settings),
        }


