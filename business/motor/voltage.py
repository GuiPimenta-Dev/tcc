from math import asin, sin

from business.base.motor import MotorBaseBusiness
from models.motor import MotorModel
from dataclasses import asdict


class Voltage(MotorBaseBusiness):
    def voltage_update(self, model: MotorModel, settings_voltage: tuple, voltage: float):
        self.__calculate_new_delta(model=model, settings_voltage=settings_voltage, voltage=voltage)

        self.__update_polar_params(model=model, voltage=voltage)

        params = {
            "polar": asdict(model.polar),
            "rect": self.rectangular_params(model=model),
        }
        return self.get_coords(params=params)

    def __calculate_new_delta(self, model: MotorModel, settings_voltage: tuple, voltage: float):
        phase = (settings_voltage[0] / voltage) * sin(self.rad(settings_voltage[1]))
        model.delta = self.degree(asin(phase))

    def __update_polar_params(self, model: MotorModel, voltage: float):
        model.Ea = voltage
        model.polar.Ea = (model.Ea, model.delta)
        model.polar.Ia = self.update_ia(model=model)
        model.Ia, model.theta = model.polar.Ia
        model.polar.RaIa = self.calculate_raia(model=model)
        model.polar.jXsIa = self.calculate_jxsia(model=model)
