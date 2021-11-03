from business.motor import MotorBusiness


class MotorService(MotorBusiness):
    def __init__(self, params: dict):
        self.settings = self.load = self.voltage = self.power_factor = self.treat_params(params)

    def __repr__(self):
        motor_informations = f'Settings: {self.settings}\n'
        motor_informations += f'Load: {self.load}\n'
        motor_informations += f'Voltage: {self.voltage}\n'
        motor_informations += f'Power Factor: {self.power_factor}\n'

        return motor_informations
