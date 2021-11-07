from cmath import acos

from business.base.motor import MotorBaseBusiness


class PowerFactor(MotorBaseBusiness):

    def power_factor_update(self, params: dict):
        settings, polar_params, rect_params = params.values()
        phase = self.degree(abs(acos(settings['Fp'])))
        if settings['lagging']:
            phase *= -1

        polar_params['Ia'] = (polar_params['Ia'][0], phase)
        polar_params['Ea'] = self.calculate_ea(settings=settings, polar_params=polar_params)
        polar_params['jXsIa'] = self.calculate_jxsia(settings=settings, polar_params=polar_params)

        params = {
            'polar': polar_params,
            'rect': self.rectangular_params(settings=settings, polar_params=polar_params)
        }
        return self.get_coords(params=params)
