from cmath import rect, phase
from math import asin

from business.base.generator import GeneratorBaseBusiness
from models.generator import GeneratorModel
from dataclasses import asdict


class Load(GeneratorBaseBusiness):

    def load_update(self, model: GeneratorModel):
        model = self.__polar_params(model=model)
        params = {
            'polar': asdict(model.polar),
            'rect': self.rectangular_params(model=model)
        }
        return self.get_coords(params=params)

    def __polar_params(self, model: GeneratorModel):
        model.polar.Ia = (model.Ia, model.theta)
        model.polar.RaIa = self.calculate_raia(model=model)
        model.polar.jXsIa = self.calculate_jxsia(model=model)
        model.polar.Ea = (model.Ea, self.__calculate_ea_phase(model=model))

        model.polar.Vt = self.__calculate_vt(model=model)
        return model

    def __calculate_ea_phase(self, model: GeneratorModel):
        phase = (abs(model.Xs) * model.Ia * model.Fp) / model.Ea
        return self.degree(asin(phase))

    def __calculate_vt(self, model: GeneratorModel):
        Ea = rect(model.polar.Ea[0], self.rad(model.polar.Ea[1]))
        Ia = rect(model.polar.Ia[0], self.rad(model.polar.Ia[1]))
        Vt = Ea - model.Ra * Ia - model.Xs * Ia

        voltage_module = abs(Vt)
        voltage_phase = self.degree(phase(Vt))
        return (voltage_module, voltage_phase)
