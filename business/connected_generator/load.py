from dataclasses import asdict

from business.base.generator import GeneratorBaseBusiness
from models.generator import GeneratorModel


class Load(GeneratorBaseBusiness):

    def load_update(self, model: GeneratorModel):
        # theta, delta = self.__calculate_new_theta_and_delta(settings=settings)
        model = self.__polar_params(model)

        params = {
            'polar': asdict(model.polar),
            'rect': self.rectangular_params(model=model)
        }
        return self.get_coords(params=params)

    def __calculate_new_theta_and_delta(self, settings: dict):
        # TODO resolve equations system
        pass

    def __polar_params(self, model: GeneratorModel):
        model.polar.Vt = (model.Vt, 0)
        model.polar.Ia = (model.Ia, model.theta)
        model.polar.RaIa = self.calculate_raia(model=model)
        model.polar.jXsIa = self.calculate_jxsia(model=model)
        model.polar.Ea = self.calculate_ea(model=model)
        return model
