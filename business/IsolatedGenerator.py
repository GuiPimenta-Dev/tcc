from models.generator import GeneratorModel
from .isolated_generator.load import Load
from .isolated_generator.power_factor import PowerFactor
from .isolated_generator.voltage import Voltage
from dataclasses import asdict


class IsolatedGenerator(Load, Voltage, PowerFactor):
    def get_settings_coords(self, model: GeneratorModel):
        params = {
            'polar': asdict(model.polar),
            'rect': asdict(model.rectangular)
        }
        coords = self.get_coords(params)
        initial_voltage = float(coords['labels']['Ea'].split(' ')[0])
        sliders = self.__get_sliders(model=model, initial_voltage=initial_voltage)
        coords.update({'sliders': sliders})
        return coords

    def __get_sliders(self, model: GeneratorModel, initial_voltage: float):
        max_load = model.Ia * 1.5
        min_ea = self.__calculate_slider_min_ea(model=model)
        max_ea = model.VtN * 1.2
        return {
            'load': {'min': 0, 'max': max_load, 'value': model.Ia},
            'voltage': {'min': min_ea, 'max': max_ea, 'value': initial_voltage},
            'power_factor': {'min': 0, 'max': 1, 'value': model.Fp}
        }

    def __calculate_slider_min_ea(self, model: GeneratorModel):
        while True:
            try:
                self.voltage_update(model=model)
                model.Ea -= 1
            except ValueError:
                break

        return int(model.Ea) + 1
