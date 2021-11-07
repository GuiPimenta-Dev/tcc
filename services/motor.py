from business.Motor import MotorBusiness


class MotorService(MotorBusiness):
    def __init__(self, params: dict):
        self.settings = self.load = self.voltage = self.power_factor = self.create_motor(params)
        self.settings_coords = self.get_coords(self.settings)

    def update_load(self, load: float):
        self.load['settings']['load'] = load * 0.746 + self.load['settings']['losses']
        return self.load_update(params=self.load)

    def update_ea(self, voltage: float):
        return self.voltage_update(params=self.voltage, voltage=voltage)

    def update_fp(self, power_factor: float):
        self.power_factor['settings']['Fp'] = power_factor
        return self.power_factor_update(params=self.power_factor)
