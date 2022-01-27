from models.generator import GeneratorModel
from .isolated_generator.load import Load
from .isolated_generator.power_factor import PowerFactor
from .isolated_generator.voltage import Voltage
from utils.constants import GeneratorTuple


class IsolatedGenerator(Load, Voltage, PowerFactor):
    def get_settings_coords(self, model: GeneratorModel):
        self._calculate_scale(model=model.rectangular)

        self._update_rectangular_params(model=model)
        coords = self._get_scaled_coords(model=model)
        initial_voltage = float(coords["labels"]["Ea"].split(" ")[0])
        sliders = self.__get_sliders(model=model, initial_voltage=initial_voltage)
        coords.update({"sliders": sliders})
        return coords

    def __get_sliders(self, model: GeneratorModel, initial_voltage: float):
        max_load = self.round(model.Ia * GeneratorTuple.MAX_LOAD)
        max_ea = self.round(model.VtN * GeneratorTuple.MAX_EA)
        return {
            "load": {"min": 0, "max": max_load, "value": model.Ia},
            "voltage": {"min": 1, "max": max_ea, "value": initial_voltage},
            "power_factor": {"min": 0, "max": 1, "value": model.Fp},
        }
