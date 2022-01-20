from copy import deepcopy
from business.Motor import Motor
from models.motor import MotorModel


class MotorService(Motor):
    def __init__(self, model: MotorModel):
        self.load = deepcopy(model)
        self.voltage = deepcopy(model)
        self.power_factor = deepcopy(model)
        self.settings_coords = self.get_settings_coords(model=model)

    def update_load(self, load: float):
        self.load.hp_load = load * 0.746 + self.load.losses
        return self.load_update(model=self.load)

    def update_ea(self, voltage: float):
        return self.voltage_update(model=self.voltage, settings_voltage=self.voltage.polar.Ea, voltage=voltage)

    def update_fp(self, power_factor: float):
        self.power_factor.Fp = power_factor
        return self.power_factor_update(model=self.power_factor)
