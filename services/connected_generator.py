from copy import deepcopy
from business.ConnectedGenerator import ConnectedGenerator

class ConnectedGeneratorService(ConnectedGenerator):
    def __init__(self, params: dict):
        self.settings = self.create_generator(params)
        self.load = deepcopy(self.settings)
        self.voltage = deepcopy(self.settings)
        self.power_factor = deepcopy(self.settings)
        self.settings_coords = self.get_coords(self.settings)

    def update_load(self, load: float):
        self.load['settings']['Il'] = load
        return self.load_update(params=self.load)

    def update_ea(self, voltage: float):
        return self.voltage_update(params=self.voltage, settings_voltage=self.settings['polar']['Ea'], voltage=voltage)

    def update_fp(self, power_factor: float):
        self.power_factor['settings']['Fp'] = power_factor
        return self.power_factor_update(params=self.power_factor)