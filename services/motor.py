from business.Motor import MotorBusiness


class MotorService(MotorBusiness):
    def __init__(self, params: dict):
        self.settings = self.load = self.voltage = self.power_factor = self.treat_params(params)
        self.initial_coords = self.get_coords(self.settings)

    def __repr__(self):
        motor_informations = f'settings: {self.settings}\n'
        motor_informations += f'load: {self.load}\n'
        motor_informations += f'voltage: {self.voltage}\n'
        motor_informations += f'fp: {self.power_factor}\n'

        return motor_informations

    def update_load(self, load: float):
        self.load['settings']['load'] = load * 0.746 + self.load['settings']['losses']
        return self.load_update(params=self.load)

    def update_fp(self, power_factor: float):
        self.power_factor['settings']['Fp'] = power_factor
        return self.fp_update(params=self.power_factor)