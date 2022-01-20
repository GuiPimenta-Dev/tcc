from copy import deepcopy
from models.generator import GeneratorModel
from business.IsolatedGenerator import IsolatedGenerator


class IsolatedGeneratorService(IsolatedGenerator):
    def __init__(self, model: GeneratorModel):
        self.load = deepcopy(model)
        self.voltage = deepcopy(model)
        self.power_factor = deepcopy(model)
        self.settings_coords = self.get_settings_coords(model)

    def update_load(self, load: float):
        self.load.Ia = load
        return self.load_update(model=self.load)

    def update_ea(self, voltage: float):
        self.voltage.Ea = voltage
        return self.voltage_update(model=self.voltage)

    def update_fp(self, power_factor: float):
        self.power_factor.Fp = power_factor
        return self.power_factor_update(model=self.power_factor)
