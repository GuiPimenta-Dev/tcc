from dataclasses import asdict

from business.base.generator import GeneratorBaseBusiness
from models.generator import GeneratorModel
from math import asin
from cmath import rect, phase
from copy import deepcopy


class Voltage(GeneratorBaseBusiness):
    def voltage_update(self, model: GeneratorModel):
        delta = self.__calculate_new_delta(model=model)
        Ia = self.__calculate_new_ia(model=model, delta=delta)

        model = self.__polar_params(model=model, Ia=Ia, delta=delta)

        params = {
            'polar': asdict(model.polar),
            'rect': self.rectangular_params(model=model)
        }
        return self.get_coords(params=params)

    def __calculate_new_delta(self, model: GeneratorModel):
        return self.degree(asin((model.Ia * model.Fp * abs(model.Xs)) / model.Ea))

    def __calculate_new_ia(self, model: GeneratorModel, delta: float):
        Vt = rect(model.Vt, 0)
        Ea = rect(model.Ea, self.rad(delta))
        Ia = (Ea - Vt) / model.Z

        current_module = abs(Ia)
        current_phase = self.degree(phase(Ia))
        return (current_module, current_phase)

    def __polar_params(self, model: GeneratorModel, Ia: tuple, delta: float):
        new_model = deepcopy(model)
        new_model.polar.Vt = (model.Vt, 0)
        new_model.Ia, new_model.theta = Ia
        new_model.polar.RaIa = self.calculate_raia(model=new_model)
        new_model.polar.jXsIa = self.calculate_jxsia(model=new_model)
        new_model.polar.Ea = (model.Ea, delta)
        return new_model
