from math import asin

from business.base.motor import MotorBaseBusiness


class Load(MotorBaseBusiness):

    def load_update(self, params: dict):
        settings, polar_params, _ = params.values()
        phase = (settings['load'] * abs(settings['Z']) * 1000) / (3 * settings['Vt'] * polar_params['Ea'][0])
        phase = self.parse_revolutions(phase)

        settings['Ea_angle'] = self.degree(self.rad(-1 * self.degree(asin(phase))))

        polar_params = self.__polar_params(settings=settings, polar_params=polar_params)
        params = {
            'polar': polar_params,
            'rect': self.rectangular_params(polar_params=polar_params)
        }
        return self.get_coords(params=params)

    def __polar_params(self, settings: dict, polar_params: dict):
        polar_params['Ea'] = (settings['Ea'], settings['Ea_angle'])
        polar_params['Ia'] = self.update_ia(settings=settings)
        polar_params['RaIa'] = self.calculate_raia(settings=settings)
        polar_params['jXsIa'] = self.calculate_jxsia(settings=settings)
        return polar_params
