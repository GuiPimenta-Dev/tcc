from cmath import rect, phase
from math import asin

from business.base.generator import GeneratorBaseBusiness
from models.generator import GeneratorModel


class Load(GeneratorBaseBusiness):
    def load_update(self, model: GeneratorModel):
        self.__update_polar_params(model=model)
        self._update_rectangular_params(model=model)

        return self._get_coords(model=model)

    def __update_polar_params(self, model: GeneratorModel):
        model.polar.Ia = (model.Ia, model.theta)
        model.polar.RaIa = self._calculate_raia(model=model)
        model.polar.jXsIa = self._calculate_jxsia(model=model)
        model.polar.Ea = (model.Ea, self.__calculate_new_delta(model=model))
        model.polar.Vt = self.__calculate_new_vt(model=model)

    def __calculate_new_delta(self, model: GeneratorModel):
        phase = (abs(model.Xs) * model.Ia * model.Fp) / model.Ea
        return self.degree(asin(phase))

    def __calculate_new_vt(self, model: GeneratorModel):
        Ea = rect(model.polar.Ea[0], self.rad(model.polar.Ea[1]))
        Ia = rect(model.polar.Ia[0], self.rad(model.polar.Ia[1]))
        Vt = Ea - model.Ra * Ia - model.Xs * Ia

        return abs(Vt), self.degree(phase(Vt))
