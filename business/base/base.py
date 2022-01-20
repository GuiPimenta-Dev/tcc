from cmath import rect, phase
from math import pi, sqrt, acos
from typing import Any, Union

from models import MachineModel, PolarModel, RectangularModel


class BaseBusiness:
    scale = 0

    def _calculate_scale(self, model: RectangularModel):
        max_coord = self.__calculate_max_coord(model=model)
        self.scale = 45 / max_coord

    def _get_coords(self, model: Union[MachineModel, Any]):
        return {
            "coords": self.__get_coords(model=model.rectangular),
            "labels": self.__get_labels(model=model.polar),
        }

    def _get_scaled_coords(self, model: Union[MachineModel, Any]):
        return {
            "coords": self.__get_scaled_coords(model=model.rectangular),
            "labels": self.__get_labels(model=model.polar),
        }

    def _update_rectangular_params(self, model: Union[MachineModel, Any]):
        model.rectangular.Vt = rect(model.polar.Vt[0], self.rad(model.polar.Vt[1]))
        model.rectangular.Ia = rect(model.polar.Ia[0], self.rad(model.polar.Ia[1]))
        model.rectangular.Ea = rect(model.polar.Ea[0], self.rad(model.polar.Ea[1]))
        model.rectangular.RaIa = rect(model.polar.RaIa[0], self.rad(model.polar.RaIa[1]))
        model.rectangular.jXsIa = rect(model.polar.jXsIa[0], self.rad(model.polar.jXsIa[1]))

    def _calculate_ia(self, model: Union[MachineModel, Any]):
        module = model.Il
        if model.delta_star == "delta":
            module = module / sqrt(3)

        phase = self.degree(acos(model.Fp))
        if model.lead_lag == "lag" and phase != 0.0:
            phase *= -1

        return module, phase

    def _calculate_raia(self, model: Union[MachineModel, Any]):
        Ia = rect(model.Ia, self.rad(model.theta))
        Ra = model.Ra * Ia

        return abs(Ra), self.degree(phase(Ra))

    def _calculate_jxsia(self, model: Union[MachineModel, Any]):
        Ia = rect(model.Ia, self.rad(model.theta))
        jXsIa = model.Xs * Ia

        return abs(jXsIa), self.degree(phase(jXsIa))

    def __get_scaled_coords(self, model: RectangularModel) -> dict:
        return {
            "Vt": (
                self.round(model.Vt.real * self.scale),
                self.round(model.Vt.imag) * self.scale,
            ),
            "Ia": (
                self.round(model.Ia.real * self.scale),
                self.round(model.Ia.imag) * self.scale,
            ),
            "Ea": (
                self.round(model.Ea.real * self.scale),
                self.round(model.Ea.imag) * self.scale,
            ),
            "RaIa": (
                self.round(model.RaIa.real * self.scale),
                self.round(model.RaIa.imag) * self.scale,
            ),
            "jXsIa": (
                self.round(model.jXsIa.real * self.scale),
                self.round(model.jXsIa.imag) * self.scale,
            ),
        }

    def __get_coords(self, model: RectangularModel) -> dict:
        max_coord = self.__calculate_max_coord(model=model)
        coef = 45 / max_coord

        return {
            "Vt": (
                self.round(model.Vt.real * coef),
                self.round(model.Vt.imag) * coef,
            ),
            "Ia": (
                self.round(model.Ia.real * coef),
                self.round(model.Ia.imag) * coef,
            ),
            "Ea": (
                self.round(model.Ea.real * coef),
                self.round(model.Ea.imag) * coef,
            ),
            "RaIa": (
                self.round(model.RaIa.real * coef),
                self.round(model.RaIa.imag) * coef,
            ),
            "jXsIa": (
                self.round(model.jXsIa.real * coef),
                self.round(model.jXsIa.imag) * coef,
            ),
        }

    def __get_labels(self, model: PolarModel):
        return {
            "Vt": f'{self.round(model.Vt[0])} ∠ {self.round(model.Vt[1])}°',
            "Ia": f'{self.round(model.Ia[0])} ∠ {self.round(model.Ia[1])}°',
            "Ea": f'{self.round(model.Ea[0])} ∠ {self.round(model.Ea[1])}°',
            "RaIa": f'{self.round(model.RaIa[0])} ∠ {self.round(model.RaIa[1])}°',
            "jXsIa": f'{self.round(model.jXsIa[0])} ∠ {self.round(model.jXsIa[1])}°',
        }

    @staticmethod
    def __calculate_max_coord(model: RectangularModel):
        max_coord = 0
        for value in model.__dict__.values():
            if abs(value.real) > max_coord:
                max_coord = abs(value.real)

            if abs(value.imag) > max_coord:
                max_coord = abs(value.imag)

        return max_coord

    @staticmethod
    def round(x: float):
        return round(x, 2)

    @staticmethod
    def degree(x: float):
        return (x * 180) / pi

    @staticmethod
    def rad(x: float):
        return (x * pi) / 180
