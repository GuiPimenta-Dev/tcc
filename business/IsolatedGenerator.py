from .isolated_generator.load import Load
from .isolated_generator.power_factor import PowerFactor
from .isolated_generator.settings import Settings
from .isolated_generator.voltage import Voltage


class IsolatedGenerator(Settings, Load, Voltage, PowerFactor):
    def get_settings_coords(self, params):
        coords = self.get_coords(params)
        initial_voltage = float(coords['labels']['Ea'].split(' ')[0])
        sliders = self.__get_sliders(params=params, initial_voltage=initial_voltage)
        coords.update({'sliders': sliders})
        return coords

    def __get_sliders(self, params: dict, initial_voltage: float):
        max_load = params['settings']['Ia'] * 1.5
        min_ea = self.__calculate_slider_min_ea(params=params)
        max_ea = params['settings']['VtN'] * 1.2
        return {
            'load': {'min': 0, 'max': max_load, 'value': params['settings']['Ia']},
            'voltage': {'min': min_ea, 'max': max_ea, 'value': initial_voltage},
            'power_factor': {'min': 0, 'max': 1, 'value': params['settings']['Fp']}
        }

    def __calculate_slider_min_ea(self, params: dict):
        while True:
            try:
                self.voltage_update(params=params)
                params['settings']['Ea'] -= 1
            except ValueError:
                break

        return int(params['settings']['Ea']) + 1
