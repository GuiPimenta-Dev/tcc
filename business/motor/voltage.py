from math import asin, sin

from business.base.motor.motor import MotorBaseBusiness


class Voltage(MotorBaseBusiness):
    def voltage_update(self, params: dict, settings_voltage: tuple, voltage: float):
        settings, polar_params, _ = params.values()
        phase = self.__calculate_ea_phase(settings_voltage=settings_voltage, voltage=voltage)

        polar_params['Ea'] = (voltage, phase)
        rect_params = self.rectangular_params(polar_params=polar_params)
        polar_params['Ia'] = self.update_ia(settings=settings, rect_params=rect_params)
        polar_params['RaIa'] = self.calculate_raia(settings=settings)
        polar_params['jXsIa'] = self.calculate_jxsia(settings=settings)

        params = {
            'polar': polar_params,
            'rect': self.rectangular_params(polar_params=polar_params)
        }
        return self.get_coords(params=params)

    def __calculate_ea_phase(self, settings_voltage: tuple, voltage: float):
        return self.degree(asin((settings_voltage[0] / voltage) * sin(self.rad(settings_voltage[1]))))



