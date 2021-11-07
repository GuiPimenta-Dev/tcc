from math import asin

from business.base.generator import GeneratorBaseBusiness


class Load(GeneratorBaseBusiness):

    def load_update(self, params: dict):
        settings, polar_params, _ = params.values()
        phase = (settings['load'] * abs(settings['Z']) * 1000) / (3 * settings['Vt'] * polar_params['Ea'][0])

        if phase > 1:
            y = int(phase)
            phase = phase - y

        phase = self.degree(self.rad(-1 * self.degree(asin(phase))))

        polar_params['Ea'] = (params['polar']['Ea'][0], phase)
        rect_params = self.rectangular_params(settings=settings, polar_params=polar_params)
        polar_params['Ia'] = self.update_ia(settings=settings, rect_params=rect_params)
        polar_params['RaIa'] = self.calculate_raia(settings=settings, polar_params=polar_params)
        polar_params['jXsIa'] = self.calculate_jxsia(settings=settings, polar_params=polar_params)

        params = {
            'polar': polar_params,
            'rect': self.rectangular_params(settings=settings, polar_params=polar_params)
        }
        return self.get_coords(params=params)
