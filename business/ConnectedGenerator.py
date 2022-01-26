from dataclasses import asdict

from models.generator import GeneratorModel
from .connected_generator.load import Load
from .connected_generator.power_factor import PowerFactor
from .connected_generator.voltage import Voltage


class ConnectedGenerator(Load, Voltage, PowerFactor):
    def get_settings_coords(self, model: GeneratorModel):
        self._calculate_scale(model=model.rectangular)
        self._update_rectangular_params(model=model)
        coords = self._get_scaled_coords(model=model)
        initial_voltage = float(coords["labels"]["Ea"].split(" ")[0])
        sliders = self.__get_sliders(model=model, initial_voltage=initial_voltage)
        coords.update({"sliders": sliders})
        return coords

    def __get_sliders(self, model: GeneratorModel, initial_voltage: float):
        max_load = model.Ia * 1.5
        min_ea = self.__calculate_slider_min_ea(model=model, settings_voltage=model.polar.Ea)
        max_ea = model.VtN * 1.2
        return {
            "load": {"min": 0, "max": max_load, "value": model.Il},
            "voltage": {"min": min_ea, "max": max_ea, "value": initial_voltage},
            "power_factor": {"min": 0, "max": 1, "value": model.Fp},
        }

    def __calculate_slider_min_ea(self, model: GeneratorModel, settings_voltage: tuple):
        voltage, _ = settings_voltage
        while True:
            try:
                self.voltage_update(model=model, settings_voltage=settings_voltage, voltage=voltage)
                voltage -= 1
            except ValueError:
                break

        return int(voltage) + 1
