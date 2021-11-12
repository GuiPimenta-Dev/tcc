from business.base.generator.connected_generator import ConnectedGeneratorBaseBusiness

class Load(ConnectedGeneratorBaseBusiness):

    def load_update(self, settings: dict, load: float):
        settings['Vt'] = self.__calculate_vt(settings=settings, load=load)
        settings['Ia'] = load
        polar_params = self.__polar_params(settings)

        params = {
            'polar': polar_params,
            'rect': self.rectangular_params(polar_params=polar_params)
        }
        return self.get_coords(params=params)


    def __calculate_vt(self, settings: dict, load: float):
        return (settings['Vt'] * settings['Ia']) / load


    def __polar_params(self, settings: dict):
        return {
            'Vt': (settings['Vt'], 0),
            'Ia': (settings['Ia'], settings['theta']),
            'RaIa': self.calculate_raia(settings=settings),
            'jXsIa': self.calculate_jxsia(settings=settings),
            'Ea': self.calculate_ea(settings=settings),
        }




