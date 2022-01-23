from cmath import rect, polar
from math import asin, sin

from business.base.generator import GeneratorBaseBusiness
from models.generator import GeneratorModel


class Voltage(GeneratorBaseBusiness):
    def voltage_update(self, model: GeneratorModel, settings_voltage: tuple, voltage: float):
        self.__calculate_new_delta(model=model, settings_voltage=settings_voltage, voltage=voltage)
        self.__calculate_new_ia_and_theta(model=model)
        self.__update_polar_params(model=model, voltage=voltage)
        self._update_rectangular_params(model=model)

        return self._get_scaled_coords(model=model)

    def __calculate_new_delta(self, model: GeneratorModel, settings_voltage: tuple, voltage: float):
        phase = (settings_voltage[0] / voltage) * sin(self.rad(settings_voltage[1]))
        model.Ea = voltage
        model.delta = self.degree(asin(phase))

    def __calculate_new_ia_and_theta(self, model: GeneratorModel):
        Ia = polar((rect(model.Ea, self.rad(model.delta)) - (rect(model.Vt, 0))) / model.Z)
        model.Ia, model.theta = Ia[0], self.degree(Ia[1])

    def __update_polar_params(self, model: GeneratorModel, voltage: float):
        model.polar.Ea = (model.Ea, model.delta)
        model.polar.Ia = (model.Ia, model.theta)
        model.polar.RaIa = self._calculate_raia(model=model)
        model.polar.jXsIa = self._calculate_jxsia(model=model)
