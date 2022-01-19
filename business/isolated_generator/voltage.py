from cmath import polar
from cmath import rect
from dataclasses import asdict

from business.base.generator import GeneratorBaseBusiness
from models.generator import GeneratorModel


class Voltage(GeneratorBaseBusiness):
    def voltage_update(self, model: GeneratorModel):
        self.__calculate_new_Ia(model=model)
        self.__calculate_new_Vt(model=model)
        self.__calculate_new_theta(model=model)

        self.__update_polar_params(model=model)

        params = {
            "polar": asdict(model.polar),
            "rect": self.rectangular_params(model=model),
        }

        return self.get_coords(params=params)

    def __calculate_new_Ia(self, model: GeneratorModel):
        Ia = polar(complex(model.Ea, 0) / (model.Z + model.Zl))
        model.Ia, model.phi = Ia[0], self.degree(Ia[1])

    def __calculate_new_Vt(self, model: GeneratorModel):
        Vt = polar(rect(model.Ea, 0) - (model.Z * rect(model.Ia, self.rad(model.phi))))
        model.Vt, model.delta = Vt[0], self.degree(Vt[1])

    def __calculate_new_theta(self, model: GeneratorModel):
        model.theta = model.phi - model.delta

    def __update_polar_params(self, model: GeneratorModel):
        model.polar.Vt = (model.Vt, 0)
        model.polar.Ia = (model.Ia, model.theta)
        model.polar.Ea = (model.Ea, model.delta)
        model.polar.RaIa = self.calculate_raia(model=model)
        model.polar.jXsIa = self.calculate_jxsia(model=model)
