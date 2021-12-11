from services.isolated_generator import IsolatedGeneratorService

args = {'Vt': 480, 'Il': 1200, 'Fp': 0.8, 'Xs': 0.1, 'Ra': 0.015, 'losses': 70, 'lagging': True, 'delta': False}
service = IsolatedGeneratorService(params=args)


class TestIsolatedGenerator:

    def test_motor_settings(self):
        expected_result = {
            'coords': {'Vt': (22.5, 0.0), 'Ia': (45.0, -33.74999999999999), 'Ea': (26.55, 3.993749999999999),
                       'RaIa': (0.67, -0.5062499999999999), 'jXsIa': (3.37, 4.499999999999998)},
            'labels': {'Vt': '480 ∠ 0°', 'Ia': '1200 ∠ -36.87°', 'Ea': '572.77 ∠ 8.55°', 'RaIa': '18.0 ∠ -36.87°',
                       'jXsIa': '120.0 ∠ 53.13°'}}

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
            'coords': {'Vt': (21.89, 0.0), 'Ia': (45.0, -33.74999999999999), 'Ea': (25.94, 3.993749999999999),
                       'RaIa': (0.67, -0.5062499999999999), 'jXsIa': (3.37, 4.499999999999998)},
            'labels': {'Vt': '467 ∠ 0°', 'Ia': '1200 ∠ -36.87°', 'Ea': '559.92 ∠ 8.75°', 'RaIa': '18.0 ∠ -36.87°',
                       'jXsIa': '120.0 ∠ 53.13°'}}

        result = service.update_vt(voltage=467)
        assert result == expected_result

    def test_update_fp(self):
        expected_result = {'coords': {'Vt': (18.0, 0.0), 'Ia': (45.0, 0.0), 'Ea': (18.68, 4.5), 'RaIa': (0.67, 0.0),
                                      'jXsIa': (0.0, 4.5)},
                           'labels': {'Vt': '480 ∠ 0°', 'Ia': '1200 ∠ 0.0°', 'Ea': '512.25 ∠ 13.55°',
                                      'RaIa': '18.0 ∠ 0.0°', 'jXsIa': '120.0 ∠ 90.0°'}}

        result = service.update_fp(power_factor=1)
        assert result == expected_result
