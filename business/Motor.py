from models.motor import MotorModel
from utils.constants import MotorTuple
from .motor.load import Load
from .motor.power_factor import PowerFactor
from .motor.voltage import Voltage


class Motor(Load, Voltage, PowerFactor):
    def get_settings_coords(self, model: MotorModel) -> dict:
        self._calculate_scale(model=model.rectangular)

        self._update_rectangular_params(model=model)
        coords = self._get_scaled_coords(model=model)
        initial_voltage = float(coords["labels"]["Ea"].split(" ")[0])
        sliders = self.__get_sliders(
            model=model,
            initial_voltage=initial_voltage,
        )
        coords.update({"sliders": sliders})
        return coords

    def __get_sliders(self, model: MotorModel, initial_voltage: float):
        return {
            "load": {"min": 0, "max": model.kw_load + MotorTuple.MAX_LOAD, "value": model.kw_load},
            "voltage": {
                "min": 55,
                "max": self.round(model.VtN * MotorTuple.MAX_EA),
                "value": initial_voltage,
            },
            "power_factor": {"min": 0, "max": 1, "value": model.Fp},
        }
