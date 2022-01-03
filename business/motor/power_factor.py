from cmath import acos
from dataclasses import asdict

from business.base.motor import MotorBaseBusiness
from models.motor import MotorModel


class PowerFactor(MotorBaseBusiness):

    def power_factor_update(self, model: MotorModel):
        phase = self.degree(abs(acos(model.Fp)))
        if model.lead_lag == 'lag' and phase != 0.0:
            phase *= -1

        model.theta = phase

        model = self.__polar_params(model=model)
        params = {
            'polar': asdict(model.polar),
            'rect': self.rectangular_params(model=model)
        }
        return self.get_coords(params=params)

    def __polar_params(self, model: MotorModel):
        model.polar.Ia = (model.Ia, model.theta)
        model.polar.Ea = self.calculate_ea(model=model)
        model.polar.RaIa = self.calculate_raia(model=model)
        model.polar.jXsIa = self.calculate_jxsia(model=model)
        return model
