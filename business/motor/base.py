from cmath import rect, phase
from math import sqrt, acos


from business.base.base import BaseBusiness


class MotorBaseBusiness(BaseBusiness):
    def calculate_ia(self, settings: dict):
        current_module = settings['Il'] / sqrt(3)
        current_phase = self.degree(acos(settings['Fp']))
        if settings['lagging']:
            current_phase *= -1
        return (current_module, current_phase)

    def calculate_ea(self, settings: dict, polar_params: dict):
        Vt = rect(settings['Vt'], self.rad(0))
        jXs = rect(settings['Z'], self.rad(90))
        Ia = rect(polar_params['Ia'][0], self.rad(polar_params['Ia'][1]))
        Ea = Vt - jXs * Ia

        voltage_module = abs(Ea)
        voltage_phase = self.degree(phase(Ea))
        return (voltage_module, voltage_phase)

    def calculate_jxsia(self, settings: dict, polar_params: dict):
        jXs = rect(settings['Xs'], self.rad(90))
        Ia = rect(polar_params['Ia'][0], self.rad(polar_params['Ia'][1]))
        jXsIa = jXs * Ia

        reactive_power_module = abs(jXsIa)
        reactive_power_phase = self.degree(phase(jXsIa))
        return (reactive_power_module, reactive_power_phase)
