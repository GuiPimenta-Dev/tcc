from business.base.generator import GeneratorBaseBusiness

class Load(GeneratorBaseBusiness):

    def load_update(self, settings: dict):
        theta, delta = self.__calculate_new_theta_and_delta(settings=settings)
        polar_params = self.__polar_params(settings)

        params = {
            'polar': polar_params,
            'rect': self.rectangular_params(polar_params=polar_params)
        }
        return self.get_coords(params=params)


    def __calculate_new_theta_and_delta(self, settings: dict):
        # TODO resolve equations system
        pass

    def __polar_params(self, settings: dict):
        return {
            'Vt': (settings['Vt'], 0),
            'Ia': (settings['Ia'], settings['Ia_angle']),
            'RaIa': self.calculate_raia(settings=settings),
            'jXsIa': self.calculate_jxsia(settings=settings),
            'Ea': self.calculate_ea(settings=settings),
        }




