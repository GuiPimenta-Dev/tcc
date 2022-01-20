from cmath import rect, phase
from math import pi, sqrt, acos
from typing import Any, Union

from models import MachineModel, PolarModel, RectangularModel
from utils.constants import DECIMAL_HOUSES


class BaseBusiness:
    def _get_coords(self, model: Union[MachineModel, Any]):
        return {
            "coords": self.__get_coords(model=model.rectangular),
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

    def __get_coords(self, model: RectangularModel) -> dict:
        max_coord = 0
        for value in model.__dict__.values():
            if abs(value.real) > max_coord:
                max_coord = abs(value.real)

            if abs(value.imag) > max_coord:
                max_coord = abs(value.imag)

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
    def round(x: float):
        return round(x, DECIMAL_HOUSES)

    @staticmethod
    def degree(x: float):
        return (x * 180) / pi

    @staticmethod
    def rad(x: float):
        return (x * pi) / 180
