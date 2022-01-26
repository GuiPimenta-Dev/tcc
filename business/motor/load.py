from math import asin

from business.base.motor import MotorBaseBusiness
from models.motor import MotorModel


class Load(MotorBaseBusiness):
    def load_update(self, model: MotorModel):
        self.__calculate_new_delta(model=model)
        self.__update_polar_params(model=model)
        self._update_rectangular_params(model=model)

        return self._get_scaled_coords(model=model)

    def __calculate_new_delta(self, model: MotorModel):
        phase = (model.hp_load * abs(model.Xs) * 1000) / (3 * model.Vt * model.Ea)
        model.delta = self.degree(self.rad(-1 * self.degree(asin(phase))))

    def __update_polar_params(self, model: MotorModel):
        model.polar.Ea = (model.Ea, model.delta)
        model.polar.Ia = self.update_ia(model=model)
        model.Ia, model.theta = model.polar.Ia
        model.polar.RaIa = self._calculate_raia(model=model)
        model.polar.jXsIa = self._calculate_jxsia(model=model)
