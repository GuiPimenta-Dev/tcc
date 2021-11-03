from business.motor import MotorBusiness


class MotorService(MotorBusiness):
    def __init__(self, params: dict):
        initial_params = self.treat_params(params)
        self.settings = initial_params
        self.load = initial_params
        self.voltage = initial_params
        self.power_factor = initial_params


    def __repr__(self):
        motor_informations = f'Settings: {self.settings}\n'
        motor_informations += f'Load: {self.load}\n'
        motor_informations += f'Voltage: {self.voltage}\n'
        motor_informations += f'Power Factor: {self.power_factor}\n'

        return motor_informations
