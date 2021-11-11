from copy import deepcopy
from business.IsolatedGenerator import IsolatedGenerator


class IsolatedGeneratorService(IsolatedGenerator):
    def __init__(self, params: dict):
        self.settings = self.create_generator(params)
        self.load = deepcopy(self.settings)
        self.voltage = deepcopy(self.settings)
        self.power_factor = deepcopy(self.settings)
        self.settings_coords = self.get_coords(self.settings)

    def update_load(self, load: float):
        self.load['settings']['Ia'] = load
        return self.load_update(params=self.load)

    def update_ea(self, voltage: float):
        self.voltage['settings']['Vt'] = voltage
        self.voltage['polar']['Vt'] = (voltage, self.voltage['polar']['Vt'][1])
        return self.voltage_update(params=self.voltage)

    def update_fp(self, power_factor: float):
        self.power_factor['settings']['Fp'] = power_factor
        return self.power_factor_update(params=self.power_factor)
