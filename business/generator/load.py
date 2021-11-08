from cmath import phase, rect

from business.base.generator import GeneratorBaseBusiness


class Load(GeneratorBaseBusiness):

    def load_update(self, params: dict):
        settings, polar_params, _ = params.values()

        polar_params['Ia'] = self.__update_ia(settings=settings, polar_params=polar_params)
        polar_params['RaIa'] = self.calculate_raia(settings=settings, polar_params=polar_params)
        polar_params['jXsIa'] = self.calculate_jxsia(settings=settings, polar_params=polar_params)
        polar_params['Vt'] = self.calculate_connected_vt(settings=settings, polar_params=polar_params)

        params = {
            'polar': polar_params,
            'rect': self.rectangular_params(polar_params=polar_params)
        }
        return self.get_coords(params=params)

    def __update_ia(self, settings: dict, polar_params: dict):
        return (settings['Il'], polar_params['Ia'][1])

    def calculate_connected_vt(self, settings: dict, polar_params: dict):
        Ea = rect(polar_params['Ea'][0], self.rad(polar_params['Ea'][1]))
        Ia = rect(polar_params['Ia'][0], self.rad(polar_params['Ia'][1]))
        Vt = Ea - settings['Ra'] * Ia - settings['Xs'] * Ia

        voltage_module = abs(Vt)
        voltage_phase = self.degree(phase(Vt))
        return (voltage_module, voltage_phase)
