from business.base.generator import GeneratorBaseBusiness


class Voltage(GeneratorBaseBusiness):
    def voltage_update(self, params: dict):
        settings, polar_params, _ = params.values()

        polar_params = self.__polar_params(settings=settings, polar_params=polar_params)

        params = {
            'polar': polar_params,
            'rect': self.rectangular_params(polar_params=polar_params)
        }

        return self.get_coords(params=params)

    def __polar_params(self, settings: dict, polar_params: dict):
        polar_params['Ea'] = self.calculate_ea(settings=settings)
        return polar_params
