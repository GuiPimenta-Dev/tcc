from cmath import phase, rect, polar

from business.base.base import BaseBusiness


class MotorBaseBusiness(BaseBusiness):
    def update_ia(self, settings: dict):
        Ia = polar((rect(settings['Vt'], 0) - rect(settings['Ea'], self.rad(settings['Ea_angle']))) / settings['Z'])

        return (Ia[0], self.degree(Ia[1]))

    def calculate_ea(self, settings: dict):
        Vt = rect(settings['Vt'], self.rad(0))
        Ia = rect(settings['Ia'], self.rad(settings['Ia_angle']))
        Ea = Vt - settings['Ra'] * Ia - settings['Xs'] * Ia

        voltage_module = abs(Ea)
        voltage_phase = self.degree(phase(Ea))
        return (voltage_module, voltage_phase)
