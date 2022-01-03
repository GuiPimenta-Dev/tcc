from services.isolated_generator import IsolatedGeneratorService
from models.generator import GeneratorModel

args = {'Vt': 480, 'Il': 1200, 'VtN': 600, 'Fp': 0.8, 'Xs': 0.1, 'Ra': 0.015, 'losses': 70, 'lead_lag': 'lag',
        'delta_star': 'star'}

service = IsolatedGeneratorService(model=GeneratorModel(**args))


class TestIsolatedGenerator:

    def test_generator_settings(self):
        expected_result = {
            'coords': {'Vt': (22.5, 0.0), 'Ia': (45.0, -33.74999999999999), 'Ea': (26.55, 3.993749999999999),
                       'RaIa': (0.67, -0.5062499999999999), 'jXsIa': (3.37, 4.499999999999998)},
            'labels': {'Vt': '480 ∠ 0°', 'Ia': '1200 ∠ -36.87°', 'Ea': '572.77 ∠ 8.55°', 'RaIa': '18.0 ∠ -36.87°',
                       'jXsIa': '120.0 ∠ 53.13°'}, 'sliders': {'load': {'min': 0, 'max': 1800.0, 'value': 1200},
                                                               'voltage': {'min': 96, 'max': 720.0, 'value': 572.77},
                                                               'power_factor': {'min': 0, 'max': 1, 'value': 0.8}}}

        results = service.settings_coords
        assert results == expected_result

    def test_update_load(self):
        expected_result = {'coords': {'Vt': (19.94, 0.5062499999999999), 'Ia': (45.0, -33.74999999999999),
                                      'Ea': (23.99, 4.499999999999999), 'RaIa': (0.67, -0.5062499999999999),
                                      'jXsIa': (3.37, 4.499999999999999)},
                           'labels': {'Vt': '468.06 ∠ 1.45°', 'Ia': '1320 ∠ -36.87°', 'Ea': '572.77 ∠ 10.62°',
                                      'RaIa': '19.8 ∠ -36.87°', 'jXsIa': '132.0 ∠ 53.13°'}}

        result = service.update_load(load=1320)
        assert result == expected_result

    def test_update_vt(self):
        expected_result = {
            'coords': {'Vt': (20.75, 0.0), 'Ia': (45.0, -33.74999999999999), 'Ea': (21.42, 4.499999999999998),
                       'RaIa': (0.67, 0.0), 'jXsIa': (0.0, 4.499999999999998)},
            'labels': {'Vt': '442.63 ∠ 0°', 'Ia': '1200 ∠ -36.87°', 'Ea': '467 ∠ 11.86°', 'RaIa': '14.4 ∠ 0.0°',
                       'jXsIa': '96.0 ∠ 90.0°'}}

        result = service.update_vt(voltage=467)
        assert result == expected_result

    def test_update_fp(self):
        expected_result = {'coords': {'Vt': (18.0, 0.0), 'Ia': (45.0, 0.0), 'Ea': (18.68, 4.5), 'RaIa': (0.67, 0.0),
                                      'jXsIa': (0.0, 4.5)},
                           'labels': {'Vt': '480 ∠ 0°', 'Ia': '1200 ∠ 0.0°', 'Ea': '512.25 ∠ 13.55°',
                                      'RaIa': '18.0 ∠ 0.0°', 'jXsIa': '120.0 ∠ 90.0°'}}

        result = service.update_fp(power_factor=1)
        assert result == expected_result
