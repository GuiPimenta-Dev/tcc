from dataclasses import dataclass

from business.base.generator import GeneratorBaseBusiness
from . import PolarModel, RectangularModel, polar_params, rectangular_params


@dataclass
class GeneratorModel(GeneratorBaseBusiness):
    Vt: float
    VtN: float
    Il: float
    Fp: float
    lead_lag: str
    delta_star: str
    Xs: [float, complex]
    Ra: [float, complex]
    losses: float

    Ia: float = None
    theta: float = None
    Ea: float = None
    delta: float = None
    phi: float = None
    polar: PolarModel = None
    rectangular: RectangularModel = None

    def __post_init__(self):
        self.Xs = complex(0, self.Xs)
        self.Ra = complex(self.Ra, 0)
        self.Ia, self.theta = self._calculate_ia(model=self)
        self.Ea, self.delta = self.calculate_new_ea_and_delta(model=self)
        self.phi = self.delta + self.theta
        self.polar = polar_params(model=self)
        self.rectangular = rectangular_params(model=self)

    @property
    def Z(self):
        return self.Ra + self.Xs

    @property
    def Zl(self):
        return self.rectangular.Vt / self.rectangular.Ia
