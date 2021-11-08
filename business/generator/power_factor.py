from cmath import acos

from business.base.generator import GeneratorBaseBusiness


class PowerFactor(GeneratorBaseBusiness):

    def power_factor_update(self, params: dict):
        settings, polar_params, rect_params = params.values()
        phase = self.degree(abs(acos(settings['Fp'])))
        if settings['lagging'] and phase != 0.0:
           phase *= -1

        polar_params['Ia'] = (polar_params['Ia'][0], phase)
        polar_params['RaIa'] = self.calculate_raia(settings=settings, polar_params=polar_params)
        polar_params['jXsIa'] = self.calculate_jxsia(settings=settings, polar_params=polar_params)
        if settings['isolated']:
            polar_params['Vt'] = self.calculate_isolated_vt_module(settings=settings, polar_params=polar_params)

        params = {
            'polar': polar_params,
            'rect': self.rectangular_params(polar_params=polar_params)
        }
        return self.get_coords(params=params)
