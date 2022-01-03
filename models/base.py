from dataclasses import dataclass
from cmath import rect
from math import sqrt

@dataclass
class PolarModel:
    Vt: tuple
    Ia: tuple
    Ea: tuple
    jXsIa: tuple
    RaIa: tuple


@dataclass
class RectangularModel:
    Vt: complex
    Ia: complex
    Ea: complex
    jXsIa: complex
    RaIa: complex

def polar_params(model):
    params = {
        'Vt': (model.Vt, 0),
        'Ia': (model.Ia, model.theta),
        'Ea': (model.Ea, model.delta),
        'RaIa': model.calculate_raia(model=model),
        'jXsIa': model.calculate_jxsia(model=model),
    }
    return PolarModel(**params)

def rectangular_params(model):
    params = {
        'Vt': rect(model.polar.Vt[0], model.rad(model.polar.Vt[1])),
        'Ia': rect(model.polar.Ia[0], model.rad(model.polar.Ia[1])),
        'Ea': rect(model.polar.Ea[0], model.rad(model.polar.Ea[1])),
        'RaIa': rect(model.polar.RaIa[0], model.rad(model.polar.RaIa[1])),
        'jXsIa': rect(
            model.polar.jXsIa[0], model.rad(model.polar.jXsIa[1])
        ),
    }

    return RectangularModel(**params)
