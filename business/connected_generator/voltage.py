from dataclasses import asdict

from business.base.generator import GeneratorBaseBusiness
from models.generator import GeneratorModel
from math import asin
from cmath import rect, phase
from copy import deepcopy


class Voltage(GeneratorBaseBusiness):
    def voltage_update(self, model: GeneratorModel):
        self.__calculate_new_delta(model=model)
        self.__calculate_new_ia_and_theta(model=model)
        self.__update_polar_params(model=model)

        params = {
            "polar": asdict(model.polar),
            "rect": self.rectangular_params(model=model),
        }
        return self.get_coords(params=params)

    def __calculate_new_delta(self, model: GeneratorModel):
        model.delta = self.degree(asin((model.Ia * model.Fp * abs(model.Xs)) / model.Ea))

    def __calculate_new_ia_and_theta(self, model: GeneratorModel):
        Vt = rect(model.Vt, 0)
        Ea = rect(model.Ea, self.rad(model.delta))
        Ia = (Ea - Vt) / model.Z

        model.Ia, model.theta = abs(Ia), self.degree(phase(Ia))

    def __update_polar_params(self, model: GeneratorModel):
        model.polar.Ea = (model.Ea, model.delta)
        model.polar.Ia = (model.Ia, model.theta)
        model.polar.RaIa = self.calculate_raia(model=model)
        model.polar.jXsIa = self.calculate_jxsia(model=model)
