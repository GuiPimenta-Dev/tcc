from business.base.generator.connected_generator import ConnectedGeneratorBaseBusiness


class Voltage(ConnectedGeneratorBaseBusiness):
    def voltage_update(self, settings: dict, voltage: float):
        settings['Ia'] = self.__calculate_ia(settings=settings, voltage=voltage)
        settings['Vt'] = voltage
        polar_params = self.__polar_params(settings)

        params = {
            'polar': polar_params,
            'rect': self.rectangular_params(polar_params=polar_params)
        }
        return self.get_coords(params=params)

    def __calculate_ia(self, settings: dict, voltage: float):
        return (settings['Vt'] * settings['Ia']) / voltage

    def __polar_params(self, settings: dict):
        return {
            'Vt': (settings['Vt'], 0),
            'Ia': (settings['Ia'], settings['theta']),
            'RaIa': self.calculate_raia(settings=settings),
            'jXsIa': self.calculate_jxsia(settings=settings),
            'Ea': self.calculate_ea(settings=settings),
        }
