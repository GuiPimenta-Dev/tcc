from .motor.load import Load
from .motor.power_factor import PowerFactor
from .motor.settings import Settings
from .motor.voltage import Voltage


class Motor(Settings, Load, Voltage, PowerFactor):
    def get_settings_coords(self, params, settings_voltage):
        coords = self.get_coords(params)
        initial_voltage = float(coords['labels']['Ea'].split(' ')[0])
        sliders = self.__get_sliders(params=params, settings_voltage=settings_voltage, initial_voltage=initial_voltage)
        coords.update({'sliders': sliders})
        return coords

    def __get_sliders(self, params: dict, settings_voltage: tuple, initial_voltage: float):
        max_load = self.__calculate_slider_max_load(params=params)
        min_ea = self.__calculate_slider_min_ea(params=params, settings_voltage=settings_voltage)
        return {
            'load': {'min': 0, 'max': max_load, 'value': params['settings']['kw_load']},
            'voltage': {'min': min_ea, 'max': params['settings']['VtN'] * 1.2, 'value': initial_voltage},
            'power_factor': {'min': 0, 'max': 1, 'value': params['settings']['Fp']}
        }

    def __calculate_slider_max_load(self, params):
        params['settings']['load'] = params['settings']['losses']
        while True:
            try:
                self.load_update(params=params)
                params['settings']['load'] += 1
            except ValueError:
                break

        return int((params['settings']['load'] / 0.746) - params['settings']['losses']) - 1

    def __calculate_slider_min_ea(self, params: dict, settings_voltage: tuple):
        voltage = settings_voltage[0]
        while True:
            try:
                self.voltage_update(params=params, settings_voltage=settings_voltage, voltage=voltage)
                voltage -= 1
            except ValueError:
                break

        return int(voltage) + 1
