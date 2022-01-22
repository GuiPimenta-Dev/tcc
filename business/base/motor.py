from cmath import phase, rect, polar
from business.base.base import BaseBusiness


class MotorBaseBusiness(BaseBusiness):
    def update_ia(self, model):
        Ia = polar((rect(model.Vt, 0) - rect(model.Ea, self.rad(model.delta))) / model.Z)

        return (Ia[0], self.degree(Ia[1]))

    def calculate_ea(self, model):
        Vt = rect(model.Vt, self.rad(0))
        Ia = rect(model.Ia, self.rad(model.theta))
        Ea = Vt - model.Ra * Ia - model.Xs * Ia

        voltage_module = abs(Ea)
        voltage_phase = self.degree(phase(Ea))
        return (voltage_module, voltage_phase)

