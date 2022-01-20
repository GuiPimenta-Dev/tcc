from typing import NamedTuple

API_ROUTE_PREFIX = "/api/v1"
MOTOR_ROUTE_PREFIX = "/api/v1/motor"
ISOLATED_GENERATOR_ROUTE_PREFIX = "/api/v1/isolated_generator"
CONNECTED_GENERATOR_ROUTE_PREFIX = "/api/v1/connected_generator"


class MotorTuple(NamedTuple):
    MAX_LOAD = 20
    MAX_EA = 1.2


class GeneratorTuple(NamedTuple):
    MAX_LOAD = 1.5
    MAX_EA = 1.2
