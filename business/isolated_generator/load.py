from cmath import rect

from business.base.isolated_generator import IsolatedGeneratorBaseBusiness


class Load(IsolatedGeneratorBaseBusiness):

    def load_update(self, params: dict):
        settings, polar_params, _ = params.values()

        polar_params['Ia'] = self._update_ia(settings=settings, polar_params=polar_params)
        polar_params['RaIa'] = self.calculate_raia(settings=settings, polar_params=polar_params)
        polar_params['jXsIa'] = self.calculate_jxsia(settings=settings, polar_params=polar_params)
        polar_params['Vt'] = self.__calculate_isolated_vt(settings=settings, polar_params=polar_params)

        params = {
            'polar': polar_params,
            'rect': self.rectangular_params(polar_params=polar_params)
        }
        return self.get_coords(params=params)


    def __calculate_isolated_vt(self, settings: dict, polar_params: dict):
        Ea = rect(polar_params['Ea'][0], self.rad(polar_params['Ea'][1]))
        Ia = rect(polar_params['Ia'][0], self.rad(polar_params['Ia'][1]))
        Vt = Ea - settings['Ra'] * Ia - settings['Xs'] * Ia

        voltage_module = abs(Vt)
        return (voltage_module, 0)



