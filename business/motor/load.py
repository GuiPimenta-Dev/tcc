from math import asin

from business.base.motor import MotorBaseBusiness
from models.motor import MotorModel
from dataclasses import asdict


class Load(MotorBaseBusiness):
    def load_update(self, model: MotorModel):
        self.__calculate_new_delta(model=model)
        self.__update_polar_params(model=model)

        params = {
            "polar": asdict(model.polar),
            "rect": self.rectangular_params(model=model),
        }
        return self.get_coords(params=params)

    def __calculate_new_delta(self, model: MotorModel):
        phase = (model.hp_load * abs(model.Z) * 1000) / (3 * model.Vt * model.polar.Ea[0])
        model.delta = self.degree(self.rad(-1 * self.degree(asin(phase))))

    def __update_polar_params(self, model: MotorModel):
        model.polar.Ea = (model.Ea, model.delta)
        model.polar.Ia = self.update_ia(model=model)
        model.Ia, model.theta = model.polar.Ia
        model.polar.RaIa = self.calculate_raia(model=model)
        model.polar.jXsIa = self.calculate_jxsia(model=model)
