from business.base.generator import GeneratorBaseBusiness


class Voltage(GeneratorBaseBusiness):
    def voltage_update(self, params: dict):
        settings, polar_params, _ = params.values()

        polar_params['Ea'] = self.calculate_ea(settings=settings)
        params = {
            'polar': polar_params,
            'rect': self.rectangular_params(polar_params=polar_params)
        }

        return self.get_coords(params=params)
