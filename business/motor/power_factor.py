from cmath import acos

from business.base.motor import MotorBaseBusiness


class PowerFactor(MotorBaseBusiness):

    def power_factor_update(self, params: dict):
        settings, polar_params, rect_params = params.values()
        phase = self.degree(abs(acos(settings['Fp'])))
        if settings['lagging'] and phase != 0.0:
            phase *= -1

        settings['theta'] = phase

        polar_params = self.__polar_params(settings=settings, polar_params=polar_params)
        params = {
            'polar': polar_params,
            'rect': self.rectangular_params(polar_params=polar_params)
        }
        return self.get_coords(params=params)

    def __polar_params(self, settings: dict, polar_params: dict):
        polar_params['Ia'] = (settings['Ia'], settings['theta'])
        polar_params['Ea'] = self.calculate_ea(settings=settings)
        polar_params['RaIa'] = self.calculate_raia(settings=settings)
        polar_params['jXsIa'] = self.calculate_jxsia(settings=settings)
        return polar_params
