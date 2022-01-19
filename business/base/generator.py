from cmath import rect, phase
from dataclasses import asdict
from math import asin

from business.base.base import BaseBusiness


class GeneratorBaseBusiness(BaseBusiness):
    def calculate_new_ea_and_delta(self, model):
        Vt = rect(model.Vt, 0)
        Ia = rect(model.Ia, self.rad(model.theta))
        Ea = Vt + model.Ra * Ia + model.Xs * Ia

        return abs(Ea), self.degree(phase(Ea))

    def power_factor_update(self, model):
        self.__update_polar_params(model=model)

        params = {
            "polar": asdict(model.polar),
            "rect": self.rectangular_params(model=model),
        }

        return self.get_coords(params=params)

    def __update_polar_params(self, model):
        model.Ia, model.theta = self.calculate_ia(model=model)
        model.polar.Ia = (model.Ia, model.theta)
        model.polar.RaIa = self.calculate_raia(model=model)
        model.polar.jXsIa = self.calculate_jxsia(model=model)
        model.polar.Ea = self.calculate_new_ea_and_delta(model=model)

    def calculate_new_delta(self, model):
        return self.degree(asin((model.Ia * model.Fp * abs(model.Xs)) / model.Ea))
