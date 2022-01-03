from cmath import rect, phase
from copy import deepcopy
from dataclasses import asdict
from math import sin, sqrt, cos, acos

from business.base.generator import GeneratorBaseBusiness
from models.generator import GeneratorModel


class Voltage(GeneratorBaseBusiness):
    def voltage_update(self, model: GeneratorModel):
        # TODO fix this logic
        delta = self.calculate_new_delta(model=model)
        Ia_cos_theta = model.Ia * model.Fp
        Ia_sin_theta = self.__calculate_ia_sin_theta(model=model, delta=delta, Ia_cos_theta=Ia_cos_theta)
        Ia = self.__calculate_ia(Ia_sin_theta=Ia_sin_theta, Ia_cos_theta=Ia_cos_theta)
        Vt = self.__calculate_vt(model=model, Ia_sin_theta=Ia_sin_theta, Ia_cos_theta=Ia_cos_theta, delta=delta)
        model = self.__polar_params(model=model, Vt=Vt, Ia=Ia, delta=delta)

        params = {
            'polar': asdict(model.polar),
            'rect': self.rectangular_params(model=model)
        }

        return self.get_coords(params=params)

    def __calculate_ia_sin_theta(self, model: GeneratorModel, delta: float, Ia_cos_theta: float):
        Ea_sin_theta = model.Ea * sin(self.rad(delta))
        Xs_Ia_cos_theta = abs(model.Xs) * Ia_cos_theta
        return (Ea_sin_theta - Xs_Ia_cos_theta) / abs(model.Ra)

    def __calculate_ia(self, Ia_sin_theta, Ia_cos_theta):
        module_ia = sqrt(abs(Ia_cos_theta) ** 2 + abs(Ia_sin_theta) ** 2)
        phase_ia = acos(Ia_cos_theta / module_ia)
        return (module_ia, phase_ia)

    def __calculate_vt(self, model: GeneratorModel, Ia_sin_theta, Ia_cos_theta, delta):
        Ea_cos_delta = model.Ea * cos(self.rad(delta))
        Vt = Ea_cos_delta - (abs(model.Ra) * Ia_cos_theta) - (abs(model.Xs) * Ia_sin_theta)
        return (Vt, 0)

    def __polar_params(self, model: GeneratorModel, Ia: tuple, Vt: tuple, delta):
        new_model = deepcopy(model)
        new_model.polar.Vt = Vt
        new_model.Ia, new_model.theta = Ia
        new_model.polar.RaIa = self.calculate_raia(model=new_model)
        new_model.polar.jXsIa = self.calculate_jxsia(model=new_model)
        new_model.polar.Ea = (model.Ea, delta)
        return new_model

