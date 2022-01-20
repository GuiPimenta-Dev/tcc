from cmath import acos

from business.base.motor import MotorBaseBusiness
from models.motor import MotorModel


class PowerFactor(MotorBaseBusiness):
    def power_factor_update(self, model: MotorModel):
        phase = self.degree(abs(acos(model.Fp)))
        if model.lead_lag == "lag" and phase != 0.0:
            phase *= -1

        self.__update_polar_params(model=model, phase=phase)
        self._update_rectangular_params(model=model)

        return self._get_scaled_coords(model=model)

    def __update_polar_params(self, model: MotorModel, phase: float):
        model.theta = phase
        model.polar.Ia = (model.Ia, model.theta)
        model.polar.Ea = self.calculate_ea(model=model)
        model.polar.RaIa = self._calculate_raia(model=model)
        model.polar.jXsIa = self._calculate_jxsia(model=model)
