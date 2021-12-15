from .connected_generator.load import Load
from .connected_generator.power_factor import PowerFactor
from .connected_generator.settings import Settings
from .connected_generator.voltage import Voltage


class ConnectedGenerator(Settings, Load, Voltage, PowerFactor):
    def get_settings_coords(self, params):
        coords = self.get_coords(params)
        initial_voltage = float(coords['labels']['Ea'].split(' ')[0])
        sliders = self.__get_sliders(params=params, initial_voltage=initial_voltage)
        coords.update({'sliders': sliders})
        return coords

    def __get_sliders(self, params: dict, initial_voltage: float):
        # max_load = self.__calculate_slider_max_load(params=params)
        #TODO change max load
        min_ea = self.__calculate_slider_min_ea(params=params)
        return {
            'load': {'min': 0, 'max': 2000, 'value': params['settings']['Ia']},
            'voltage': {'min': min_ea, 'max': params['settings']['VtN'] * 1.2, 'value': initial_voltage},
            'power_factor': {'min': 0, 'max': 1, 'value': params['settings']['Fp']}
        }

    # def __calculate_slider_max_load(self, params):
    #     params['settings']['load'] = params['settings']['losses']
    #     while True:
    #         try:
    #             self.load_update(params=params)
    #             params['settings']['load'] += 1
    #         except ValueError:
    #             break
    #
    #     return int((params['settings']['load'] / 0.746) - params['settings']['losses']) - 1

    def __calculate_slider_min_ea(self, params: dict):
        while True:
            try:
                self.voltage_update(settings=params['settings'])
                params['settings']['Ea'] -= 1
            except ValueError:
                break

        return int(params['settings']['Ea']) + 1
