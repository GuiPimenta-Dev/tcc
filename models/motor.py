from dataclasses import dataclass
from math import sqrt

from business.base.motor import MotorBaseBusiness
from . import PolarModel, RectangularModel, polar_params, rectangular_params


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

    hp_load: float = None
    Ia: float = None
    theta: float = None
    Ea: float = None
    delta: float = None
    delta_star: str = "delta"
    polar: PolarModel = None
    rectangular: RectangularModel = None

    def __post_init__(self):
        self.Xs = complex(0, self.Xs)
        self.Ra = complex(self.Ra, 0)
        self.hp_load = self.kw_load * 0.746 + self.losses
        self.Ia, self.theta = self._calculate_ia(model=self)
        self.Ea, self.delta = self.calculate_ea(model=self)
        self.polar = polar_params(model=self)
        self.rectangular = rectangular_params(model=self)

    @property
    def Il(self):
        return self.hp_load * 1000 / (sqrt(3) * self.Vt * self.Fp)

    @property
    def Z(self):
        return self.Ra + self.Xs
