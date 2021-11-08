from business.base.connected_generator import ConnectedGeneratorBaseBusiness

class Load(ConnectedGeneratorBaseBusiness):

    def load_update(self, params: dict):
        settings, polar_params, _ = params.values()

        polar_params['Ia'] = self._update_ia(settings=settings, polar_params=polar_params)
        polar_params['RaIa'] = self.calculate_raia(settings=settings, polar_params=polar_params)
        polar_params['jXsIa'] = self.calculate_jxsia(settings=settings, polar_params=polar_params)
        polar_params['Ea'] = self.calculate_connected_ea(settings=settings, polar_params=polar_params)

        params = {
            'polar': polar_params,
            'rect': self.rectangular_params(polar_params=polar_params)
        }
        return self.get_coords(params=params)



