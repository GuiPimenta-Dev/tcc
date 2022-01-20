from math import asin, sin

from business.base.motor import MotorBaseBusiness
from models.motor import MotorModel


class Voltage(MotorBaseBusiness):
    def voltage_update(self, model: MotorModel, settings_voltage: tuple, voltage: float):
        self.__calculate_new_delta(model=model, settings_voltage=settings_voltage, voltage=voltage)
        self.__update_polar_params(model=model, voltage=voltage)
        self._update_rectangular_params(model=model)

        return self._get_scaled_coords(model=model)

    def _max_voltage_update(self, model: MotorModel, settings_voltage: tuple, voltage: float):
        self.__calculate_new_delta(model=model, settings_voltage=settings_voltage, voltage=voltage)
        self.__update_polar_params(model=model, voltage=voltage)
        self._update_rectangular_params(model=model)
        return model.rectangular

    def __calculate_new_delta(self, model: MotorModel, settings_voltage: tuple, voltage: float):
        phase = (settings_voltage[0] / voltage) * sin(self.rad(settings_voltage[1]))
        model.delta = self.degree(asin(phase))

    def __update_polar_params(self, model: MotorModel, voltage: float):
        model.Ea = voltage
        model.polar.Ea = (model.Ea, model.delta)
        model.polar.Ia = self.update_ia(model=model)
        model.Ia, model.theta = model.polar.Ia
        model.polar.RaIa = self._calculate_raia(model=model)
        model.polar.jXsIa = self._calculate_jxsia(model=model)
