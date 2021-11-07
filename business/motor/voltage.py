from math import sin

from business.base.motor import MotorBaseBusiness


class Voltage(MotorBaseBusiness):
    def voltage_update(self, params: dict, voltage: float):
        settings, polar_params, _ = params.values()
        phase = self.__calculate_ea_phase(old_voltage=polar_params['Ea'], voltage=voltage)

        polar_params['Ea'] = (voltage, phase)
        rect_params = self.rectangular_params(settings=settings, polar_params=polar_params)
        polar_params['Ia'] = self.update_ia(settings=settings, rect_params=rect_params)
        polar_params['jXsIa'] = self.calculate_jxsia(settings=settings, polar_params=polar_params)

        params = {
            'polar': polar_params,
            'rect': self.rectangular_params(settings=settings, polar_params=polar_params)
        }
        return self.get_coords(params=params)

    def __calculate_ea_phase(self, old_voltage: tuple, voltage: float):
        return self.degree((old_voltage[0] / voltage) * sin(self.rad(old_voltage[1])))
