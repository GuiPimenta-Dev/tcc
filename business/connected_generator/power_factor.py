from business.base.generator.connected_generator import ConnectedGeneratorBaseBusiness


class PowerFactor(ConnectedGeneratorBaseBusiness):

    def power_factor_update(self, params: dict):
        return super(PowerFactor, self).power_factor_update(params=params)
