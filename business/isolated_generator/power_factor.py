from business.base.generator.isolated_generator import IsolatedGeneratorBaseBusiness


class PowerFactor(IsolatedGeneratorBaseBusiness):

    def power_factor_update(self, params: dict):
        return super(PowerFactor, self).power_factor_update(params=params)


