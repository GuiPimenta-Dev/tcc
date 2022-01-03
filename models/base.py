from dataclasses import dataclass


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
