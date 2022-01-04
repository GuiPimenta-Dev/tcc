from cmath import rect
from dataclasses import dataclass
from math import sqrt

from business.base.motor import MotorBaseBusiness
from .base import PolarModel, RectangularModel, polar_params, rectangular_params



@dataclass
class MotorModel(MotorBaseBusiness):
    Vt: float
    VtN: float
    Fp: float
    lead_lag: str
    Xs: [float, complex]
    Ra: [float, complex]
    kw_load: float
    losses: float

    Il: float = None
    Ia: float = None
    theta: float = None
    Ea: float = None
    delta: float = None
    Z: complex = None
    hp_load: float = None
    delta_star: str = 'delta'
    polar: PolarModel = None
    rectangular: RectangularModel = None

    def __post_init__(self):
        self.hp_load = self.kw_load * 0.746 + self.losses
        self.Xs = complex(0, self.Xs)
        self.Ra = complex(self.Ra, 0)
        self.Z = self.Ra + self.Xs
        self.Il = self.hp_load * 1000 / (sqrt(3) * self.Vt * self.Fp)
        self.Ia, self.theta = self.calculate_ia(model=self)
        self.Ea, self.delta = self.calculate_ea(model=self)
        self.polar = polar_params(model=self)
        self.rectangular = rectangular_params(model=self)

    # def __polar_params(self):
    #     params = {
    #         'Vt': (self.Vt, 0),
    #         'Ia': (self.Ia, self.theta),
    #         'Ea': (self.Ea, self.delta),
    #         'RaIa': self.calculate_raia(model=self),
    #         'jXsIa': self.calculate_jxsia(model=self),
    #     }
    #     return PolarModel(**params)
    #
    # def __rectangular_params(self):
    #     params = {
    #         'Vt': rect(self.polar.Vt[0], self.rad(self.polar.Vt[1])),
    #         'Ia': rect(self.polar.Ia[0], self.rad(self.polar.Ia[1])),
    #         'Ea': rect(self.polar.Ea[0], self.rad(self.polar.Ea[1])),
    #         'RaIa': rect(self.polar.RaIa[0], self.rad(self.polar.RaIa[1])),
    #         'jXsIa': rect(
    #             self.polar.jXsIa[0], self.rad(self.polar.jXsIa[1])
    #         ),
    #     }
    #
    #     return RectangularModel(**params)

