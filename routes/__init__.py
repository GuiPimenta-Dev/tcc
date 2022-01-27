import pickle
from typing import Union

from services.motor import MotorService
from services.connected_generator import ConnectedGeneratorService
from services.isolated_generator import IsolatedGeneratorService


def dump_model(model: Union[MotorService, ConnectedGeneratorService, IsolatedGeneratorService], machine: str):
    with open(f"models/pickle/{machine}.pickle", "wb") as f:
        pickle.dump(model, f)


def load_model(machine: str):
    with open(f"models/pickle/{machine}.pickle", "rb") as f:
        return pickle.load(f)
