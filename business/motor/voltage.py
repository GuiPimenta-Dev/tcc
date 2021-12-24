from math import asin, sin

from business.base.motor import MotorBaseBusiness


class Voltage(MotorBaseBusiness):
    def voltage_update(self, params: dict, settings_voltage: tuple, voltage: float):
        settings, polar_params, _ = params.values()
        settings['Ea_angle'] = self.__calculate_ea_phase(settings_voltage=settings_voltage, voltage=voltage)
        settings['Ea'] = voltage

        polar_params = self.__polar_params(settings=settings, polar_params=polar_params)
        params = {
            'polar': polar_params,
            'rect': self.rectangular_params(polar_params=polar_params)
        }
        return self.get_coords(params=params)

    def __polar_params(self, settings: dict, polar_params: dict):
        polar_params['Ea'] = (settings['Ea'], settings['Ea_angle'])
        polar_params['Ia'] = self.update_ia(settings=settings)
        settings['Ia'], settings['Ia_angle'] = polar_params['Ia'][0], polar_params['Ia'][1]
        polar_params['RaIa'] = self.calculate_raia(settings=settings)
        polar_params['jXsIa'] = self.calculate_jxsia(settings=settings)

        return polar_params

    def __calculate_ea_phase(self, settings_voltage: tuple, voltage: float):
        phase = (settings_voltage[0] / voltage) * sin(self.rad(settings_voltage[1]))
        return self.degree(asin(phase))



