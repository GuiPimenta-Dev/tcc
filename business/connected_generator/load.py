from dataclasses import asdict
from math import asin, sqrt, atan

from business.base.generator import GeneratorBaseBusiness
from models.generator import GeneratorModel


class Load(GeneratorBaseBusiness):
    def load_update(self, model: GeneratorModel):
        self.__calculate_new_Ea_delta(model=model)
        self.__calculate_new_Ia_and_new_theta(model=model)
        self.__update_polar_params(model)

        params = {
            "polar": asdict(model.polar),
            "rect": self.rectangular_params(model=model),
        }
        return self.get_coords(params=params)

    def __calculate_new_Ea_delta(self, model: GeneratorModel):
        model.delta = self.degree(asin((model.Ia * abs(model.Xs)) / model.Ea))

    def __calculate_new_Ia_and_new_theta(self, model: GeneratorModel):
        model.Ia, model.theta = sqrt(model.Ia ** 2 + model.rectangular.Ia.imag ** 2), self.degree(
            atan(model.rectangular.Ia.imag / model.Ia)
        )

    def __update_polar_params(self, model: GeneratorModel):
        model.polar.Ea = (model.Ea, model.delta)
        model.polar.Ia = (model.Ia, model.theta)
        model.polar.RaIa = self.calculate_raia(model=model)
        model.polar.jXsIa = self.calculate_jxsia(model=model)
