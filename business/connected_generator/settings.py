from business.base.connected_generator import ConnectedGeneratorBaseBusiness


class Settings(ConnectedGeneratorBaseBusiness):
    def create_generator(self, settings: dict):
        settings['Ia'] = self.calculate_ia_module(settings=settings)
        settings = self.calculate_impedance(settings=settings)
        polar_params = self.__connected_polar_params(settings)
        rect_params = self.rectangular_params(polar_params=polar_params)
        return {
            'settings': settings,
            'polar': polar_params,
            'rect': rect_params,
        }

    def __connected_polar_params(self, settings: dict):
        polar_params = {'Vt': (settings['Vt'], 0), 'Ia': self.calculate_ia(settings=settings)}
        polar_params['RaIa'] = self.calculate_raia(settings=settings, polar_params=polar_params)
        polar_params['jXsIa'] = self.calculate_jxsia(settings=settings, polar_params=polar_params)
        polar_params['Ea'] = self.calculate_connected_ea(settings=settings, polar_params=polar_params)

        return polar_params


