from business.base.generator import GeneratorBaseBusiness
from models.generator import GeneratorModel


class PowerFactor(GeneratorBaseBusiness):

    def power_factor_update(self, model: GeneratorModel):
        return super(PowerFactor, self).power_factor_update(model=model)
