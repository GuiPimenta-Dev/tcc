from dataclasses import asdict

from models.motor import MotorModel
from .motor.load import Load
from .motor.power_factor import PowerFactor
from .motor.voltage import Voltage


class Motor(Load, Voltage, PowerFactor):
    def get_settings_coords(self, model: MotorModel, settings_voltage: tuple) -> dict:
        params = {
            'polar': asdict(model.polar),
            'rect': asdict(model.rectangular)
        }
        coords = self.get_coords(params=params)
        initial_voltage = float(coords['labels']['Ea'].split(' ')[0])
        sliders = self.__get_sliders(model=model, settings_voltage=settings_voltage, initial_voltage=initial_voltage)
        coords.update({'sliders': sliders})
        return coords

    def __get_sliders(self, model: MotorModel, settings_voltage: tuple, initial_voltage: float):
        default_max_load = model.kw_load + 20
        max_load = self.__calculate_slider_max_load(model=model)
        max_load = max_load if max_load < default_max_load else default_max_load
        min_ea = self.__calculate_slider_min_ea(model=model, settings_voltage=settings_voltage)
        return {
            'load': {'min': 0, 'max': max_load, 'value': model.kw_load},
            'voltage': {'min': min_ea, 'max': self.round(model.VtN * 1.2), 'value': initial_voltage},
            'power_factor': {'min': 0, 'max': 1, 'value': model.Fp}
        }

    def __calculate_slider_max_load(self, model: MotorModel):
        model.hp_load = model.losses
        while True:
            try:
                self.load_update(model=model)
                model.hp_load += 1
            except ValueError:
                break

        return int((model.hp_load / 0.746) - model.losses) - 1

    def __calculate_slider_min_ea(self, model: MotorModel, settings_voltage: tuple):
        voltage, _ = settings_voltage
        while True:
            try:
                self.voltage_update(model=model, settings_voltage=settings_voltage, voltage=voltage)
                voltage -= 1
            except ValueError:
                break

        return int(voltage) + 1
