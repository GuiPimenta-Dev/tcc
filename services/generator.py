from copy import deepcopy
from business.Generator import GeneratorBusiness

class GeneratorService(GeneratorBusiness):
    def __init__(self, params: dict):
        self.settings = self.create_generator(params)
        self.load = deepcopy(self.settings)
        self.voltage = deepcopy(self.settings)
        self.power_factor = deepcopy(self.settings)
        self.settings_coords = self.get_coords(self.settings)

    def update_load(self, load: float):
        pass

    def update_ea(self, voltage: float):
        pass

    def update_fp(self, power_factor: float):
        pass