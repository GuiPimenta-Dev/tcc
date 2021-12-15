from services.connected_generator import ConnectedGeneratorService

args = {'Vt': 480, 'VtN': 600, 'Il': 1200, 'Fp': 0.8, 'Xs': 0.1, 'Ra': 0.015, 'losses': 70, 'lagging': True,
        'delta': False}
service = ConnectedGeneratorService(params=args)


class TestConnectedGenerator:

    def test_motor_settings(self):
        expected_result = {
            'coords': {'Vt': (22.5, 0.0), 'Ia': (45.0, -33.74999999999999), 'Ea': (26.55, 3.993749999999999),
                       'RaIa': (0.67, -0.5062499999999999), 'jXsIa': (3.37, 4.499999999999998)},
            'labels': {'Vt': '480 ∠ 0°', 'Ia': '1200 ∠ -36.87°', 'Ea': '572.77 ∠ 8.55°', 'RaIa': '18.0 ∠ -36.87°',
                       'jXsIa': '120.0 ∠ 53.13°'}, 'sliders': {'load': {'min': 0, 'max': 2000, 'value': 1200},
                                                               'voltage': {'min': 96, 'max': 720.0, 'value': 572.77},
                                                               'power_factor': {'min': 0, 'max': 1, 'value': 0.8}}}

        result = service.settings_coords
        assert result == expected_result

    def test_update_load(self):
        expected_result = {'coords': {'Vt': (8.1, 0.0), 'Ia': (45.0, -33.75), 'Ea': (12.15, 3.9937499999999995),
                                      'RaIa': (0.68, -0.50625), 'jXsIa': (3.37, 4.5)},
                           'labels': {'Vt': '288.0 ∠ 0°', 'Ia': '2000 ∠ -36.87°', 'Ea': '454.74 ∠ 18.2°',
                                      'RaIa': '30.0 ∠ -36.87°', 'jXsIa': '200.0 ∠ 53.13°'}}

        result = service.update_load(load=2000)
        assert result == expected_result

    def test_update_ea(self):
        expected_result = {
            'coords': {'Vt': (8.85, 0.0), 'Ia': (24.46, -45.000012469640524), 'Ea': (13.72, 1.7709132486761157),
                       'RaIa': (0.37, -0.6749762059276987), 'jXsIa': (4.5, 2.4458894546038144)},
            'labels': {'Vt': '480 ∠ 0°', 'Ia': '2776.47 ∠ -61.47°', 'Ea': '750 ∠ 7.35°', 'RaIa': '41.65 ∠ -61.47°',
                       'jXsIa': '277.65 ∠ 28.53°'}}

        result = service.update_vt(voltage=750)
        assert result == expected_result

    def test_update_fp(self):
        expected_result = {'coords': {'Vt': (18.0, 0.0), 'Ia': (45.0, 0.0), 'Ea': (18.68, 4.5), 'RaIa': (0.67, 0.0),
                                      'jXsIa': (0.0, 4.5)},
                           'labels': {'Vt': '480 ∠ 0°', 'Ia': '1200 ∠ 0.0°', 'Ea': '512.25 ∠ 13.55°',
                                      'RaIa': '18.0 ∠ 0.0°', 'jXsIa': '120.0 ∠ 90.0°'}}
        result = service.update_fp(power_factor=1)
        assert result == expected_result
