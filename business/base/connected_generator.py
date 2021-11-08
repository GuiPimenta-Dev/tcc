from cmath import phase, rect

from business.base.base import BaseBusiness


class ConnectedGeneratorBaseBusiness(BaseBusiness):
    def calculate_connected_ea(self, settings: dict, polar_params: dict):
        Vt = rect(polar_params['Vt'][0], self.rad(polar_params['Vt'][1]))
        Ia = rect(polar_params['Ia'][0], self.rad(polar_params['Ia'][1]))
        Ea = Vt + settings['Ra'] * Ia + settings['Xs'] * Ia

        voltage_module = abs(Ea)
        voltage_phase = self.degree(phase(Ea))
        return (voltage_module, voltage_phase)

